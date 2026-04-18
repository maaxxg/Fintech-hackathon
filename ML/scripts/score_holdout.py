"""
score_holdout.py

Scores holdout clients with churn model + SHAP and value model, then writes
one Firestore document per client to the `clients` collection.

Usage (from ML/ directory):
    python scripts/score_holdout.py
"""

import json
import os
import pickle
import random
import sys
import warnings
from datetime import datetime, timedelta
from pathlib import Path

import numpy as np
import pandas as pd

# ---------------------------------------------------------------------------
# Path setup so `config` is importable when run as:  cd ML && python scripts/...
# ---------------------------------------------------------------------------
_SCRIPT_DIR = Path(__file__).resolve().parent          # ML/scripts/
_ML_DIR = _SCRIPT_DIR.parent                           # ML/
sys.path.insert(0, str(_ML_DIR))

from config import PROCESSED_DATA_DIR, MODELS_DIR      # noqa: E402

# ---------------------------------------------------------------------------
# Firebase init
# ---------------------------------------------------------------------------
import firebase_admin
from firebase_admin import credentials, firestore, initialize_app

_KEY_DEFAULT = _ML_DIR.parent / "fintech-hackathon-2-firebase-adminsdk-fbsvc-5e5a462a40.json"
key_path = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS", str(_KEY_DEFAULT))
cred = credentials.Certificate(key_path)
initialize_app(cred)
db = firestore.client()

# ---------------------------------------------------------------------------
# Reference date for joinDate calculation
# ---------------------------------------------------------------------------
_REFERENCE_DATE = datetime(2026, 4, 17)

# ---------------------------------------------------------------------------
# Load holdout client IDs
# ---------------------------------------------------------------------------
print("Loading holdout IDs...")
with open(PROCESSED_DATA_DIR / "split_holdout.json") as f:
    holdout_ids: list[str] = json.load(f)
holdout_set = set(holdout_ids)
print(f"  {len(holdout_ids)} holdout clients")

# ---------------------------------------------------------------------------
# Load churn model artifacts
# ---------------------------------------------------------------------------
print("Loading churn model artifacts...")
with open(MODELS_DIR / "churn_model.pkl", "rb") as f:
    churn_model = pickle.load(f)
with open(MODELS_DIR / "churn_explainer.pkl", "rb") as f:
    churn_explainer = pickle.load(f)
with open(MODELS_DIR / "churn_feature_columns.json") as f:
    churn_feature_columns: list[str] = json.load(f)

# ---------------------------------------------------------------------------
# Load and filter features_churn
# ---------------------------------------------------------------------------
print("Loading features_churn.parquet...")
df_churn_all = pd.read_parquet(PROCESSED_DATA_DIR / "features_churn.parquet")
df_churn = df_churn_all[df_churn_all["IDENTIFIKATOR_KLIJENTA"].isin(holdout_set)].copy()
df_churn = df_churn.set_index("IDENTIFIKATOR_KLIJENTA")
print(f"  {len(df_churn)} holdout rows found in features_churn")

# ---------------------------------------------------------------------------
# Load and filter features_value
# ---------------------------------------------------------------------------
print("Loading features_value.parquet...")
df_value_all = pd.read_parquet(PROCESSED_DATA_DIR / "features_value.parquet")
df_value = df_value_all[df_value_all["IDENTIFIKATOR_KLIJENTA"].isin(holdout_set)].copy()
df_value = df_value.set_index("IDENTIFIKATOR_KLIJENTA")
print(f"  {len(df_value)} holdout rows found in features_value")

# ---------------------------------------------------------------------------
# Load and filter cashback_scores, build spending profile per client
# ---------------------------------------------------------------------------
print("Loading cashback_scores.parquet...")
df_cash_all = pd.read_parquet(PROCESSED_DATA_DIR / "cashback_scores.parquet")
df_cash = df_cash_all[df_cash_all["IDENTIFIKATOR_KLIJENTA"].isin(holdout_set)].copy()
df_cash = df_cash[df_cash["monthly_spend"] > 0]

# Pivot: for each client, sum monthly_spend per category
spending_profiles: dict[str, dict] = {}
cash_pivot = df_cash.groupby(["IDENTIFIKATOR_KLIJENTA", "KATEGORIJA"])["monthly_spend"].sum()
for (client_id, kategorija), spend in cash_pivot.items():
    if spend > 0:
        spending_profiles.setdefault(client_id, {})[kategorija] = round(float(spend), 2)
print(f"  {len(spending_profiles)} clients have spending profile data")

# ---------------------------------------------------------------------------
# Score churn: predict_proba + SHAP
# ---------------------------------------------------------------------------
print("Scoring churn model + SHAP (this may take a moment)...")

# Identify categorical columns and encode
X_all = df_churn[churn_feature_columns].copy()
cat_cols = [c for c in churn_feature_columns if X_all[c].dtype == object or str(X_all[c].dtype) == "category"]
for c in cat_cols:
    X_all[c] = X_all[c].astype("category")

churn_probs = churn_model.predict_proba(X_all)[:, 1]  # shape (n,)

with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    shap_raw = churn_explainer.shap_values(X_all)   # shape (n, n_features)

# shap_raw is a single ndarray for the positive class (LightGBM binary)
if isinstance(shap_raw, list):
    shap_matrix = np.array(shap_raw[1])
else:
    shap_matrix = np.array(shap_raw)

# Map client IDs back to scores
churn_by_id: dict[str, float] = dict(zip(df_churn.index, churn_probs.tolist()))
shap_by_id: dict[str, np.ndarray] = dict(zip(df_churn.index, shap_matrix))

print(f"  Scored {len(churn_by_id)} clients for churn")

# ---------------------------------------------------------------------------
# Helper: build top-3 SHAP explanation text
# ---------------------------------------------------------------------------
def _top3_shap_text(shap_vals: np.ndarray, feature_names: list[str]) -> tuple[str, list[dict]]:
    """Return (text, list-of-dicts) for the top 3 features by |shap|."""
    abs_vals = np.abs(shap_vals)
    top_idx = np.argsort(abs_vals)[::-1][:3]
    parts = []
    records = []
    for i in top_idx:
        name = feature_names[i]
        val = float(shap_vals[i])
        sign = "+" if val >= 0 else "-"
        parts.append(f"{name} ({sign}{abs(val):.2f})")
        records.append({"feature": name, "impact": round(val, 4)})
    text = "Top churn drivers: " + ", ".join(parts)
    return text, records


# ---------------------------------------------------------------------------
# Helper: compute joinDate from tenure_months
# ---------------------------------------------------------------------------
def _join_date(tenure_months: float) -> str:
    dt = _REFERENCE_DATE - timedelta(days=tenure_months * 30.44)
    return dt.strftime("%Y-%m-%d")


# ---------------------------------------------------------------------------
# Build Firestore docs and batch-write
# ---------------------------------------------------------------------------
print("Building Firestore documents...")

# Seed here so phone numbers are reproducible regardless of upstream random state
# (model loading and SHAP calls may consume random numbers before this point)
random.seed(42)

# Pre-generate phone numbers in holdout_ids order (reproducible)
phone_map: dict[str, str] = {}
for cid in holdout_ids:
    phone_map[cid] = f"+385 91 {random.randint(1_000_000, 9_999_999)}"

written = 0
skipped = 0
batch = db.batch()
batch_count = 0
BATCH_LIMIT = 500

for idx, client_id in enumerate(holdout_ids):
    # --- guard: must exist in both churn and value features ---
    if client_id not in churn_by_id:
        print(f"  WARNING: {client_id} missing from features_churn — skipping")
        skipped += 1
        continue
    if client_id not in df_value.index:
        print(f"  WARNING: {client_id} missing from features_value — skipping")
        skipped += 1
        continue

    # --- churn ---
    churn_prob = churn_by_id[client_id]
    shap_vals = shap_by_id[client_id]
    risk_explanation, shap_top3 = _top3_shap_text(shap_vals, churn_feature_columns)

    # --- value ---
    vrow = df_value.loc[client_id]
    value_score = float(vrow["value_score"])
    value_tier = str(vrow["value_tier"])
    tenure_months = float(vrow["tenure_months"])

    balance_score = float(vrow["balance_score"])
    revenue_score = float(vrow["revenue_score"])
    product_depth_score = float(vrow["product_depth_score"])
    tenure_score = float(vrow["tenure_score"])
    primary_bank_score = float(vrow["primary_bank_score"])
    credit_rating_score = float(vrow["credit_rating_score"])

    # --- spending profile ---
    spending_dict = spending_profiles.get(client_id, {})

    # --- derived fields ---
    join_date_str = _join_date(tenure_months)
    account_type = value_tier.capitalize()

    doc = {
        # Required by Client interface
        "managerId": "demo-manager",
        "name": f"Klijent {client_id[:6]}",
        "riskScore": int(round(churn_prob * 100)),
        "valueScore": int(round(value_score * 100)),
        "riskExplanation": risk_explanation,
        "valueExplanation": f"{account_type} tier client (score: {value_score:.2f})",
        "email": f"klijent.{client_id[:6].lower()}@banka.hr",
        "phone": phone_map[client_id],
        "accountType": account_type,
        "joinDate": join_date_str,
        # Extended profile fields
        "churn_probability": round(churn_prob, 4),
        "value_score_raw": round(value_score, 4),
        "value_tier": value_tier,
        "spending_profile": spending_dict,
        "shap_top3": shap_top3,
        "balance_score": round(balance_score, 4),
        "revenue_score": round(revenue_score, 4),
        "product_depth_score": round(product_depth_score, 4),
        "tenure_score": round(tenure_score, 4),
        "primary_bank_score": round(primary_bank_score, 4),
        "credit_rating_score": round(credit_rating_score, 4),
    }

    doc_ref = db.collection("clients").document(client_id)
    batch.set(doc_ref, doc)
    batch_count += 1
    written += 1

    # Commit when batch is full
    if batch_count >= BATCH_LIMIT:
        batch.commit()
        batch = db.batch()
        batch_count = 0

    if written % 100 == 0:
        print(f"  Queued {written} docs...")

# Commit remaining
if batch_count > 0:
    batch.commit()

print(f"\nWrote {written} docs to Firestore (skipped {skipped})")
