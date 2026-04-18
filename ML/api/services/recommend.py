import sys
import json
import math
import pickle
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from config import PROCESSED_DATA_DIR, MODELS_DIR, OFFER_CATALOG
from ModelToConfig import calculate_dynamic_cashback, _build_category_map, _match_category

OFFER_BY_CATEGORY: dict[str, dict] = {o["category"]: o for o in OFFER_CATALOG}
_OFFER_TOKENS = _build_category_map(OFFER_CATALOG)

# English category names present in parquet that fuzzy matching can't resolve
_ENGLISH_CATEGORY_MAP: dict[str, str] = {
    "Retail outlets":                                        "TRGOVINA_NA_VELIKO_I_NA_MALO",
    "Clothing outlets":                                      "TRGOVINA_NA_VELIKO_I_NA_MALO",
    "Repair services":                                       "TRGOVINA_NA_VELIKO_I_NA_MALO",
    "Transportation":                                        "PRIJEVOZ_I_SKLADISTENJE",
    "Amusement and entertainment":                           "UMJETNOST_ZABAVA_I_REKREACIJA",
    "Government services":                                   "JAVNA_UPRAVA_I_OBRANA",
    "Business services":                                     "STRUCNE_ZNANSTVENE_I_TEHNICKE_DJELATNOSTI",
    "Professional services and membership organizations":    "STRUCNE_ZNANSTVENE_I_TEHNICKE_DJELATNOSTI",
    "Agricultural services":                                 "POLJOPRIVREDA_SUMARSTVO_I_RIBARSTVO",
    "Utilities":                                             "OPSKRBA_ELEKTRICNOM_ENERGIJOM_PLINOM_PAROM_I_KLIMATIZACIJA",
    "Contracted services":                                   "OSTALE_USLUZNE_DJELATNOSTI",
    "Miscellaneous outlets":                                 "OSTALE_USLUZNE_DJELATNOSTI",
    "Service providers":                                     "OSTALE_USLUZNE_DJELATNOSTI",
    "GRAÐEVINARSTVO":                                        "OSTALE_USLUZNE_DJELATNOSTI",
    "PRERAÐIVAÈKA INDUSTRIJA":                               "OSTALE_USLUZNE_DJELATNOSTI",
}

TOP_N = 3


def _load_client_scores() -> dict[str, dict]:
    """Build per-client {value_score, churn_probability} from parquet + churn model."""
    # Value scores
    val_df = pd.read_parquet(PROCESSED_DATA_DIR / "features_value.parquet")[
        ["IDENTIFIKATOR_KLIJENTA", "value_score"]
    ]

    # Churn probabilities from trained model
    holdout_ids = set(
        json.loads((PROCESSED_DATA_DIR / "split_holdout.json").read_text())
    )
    feat_df = pd.read_parquet(PROCESSED_DATA_DIR / "features_churn.parquet")
    feat_df = feat_df[feat_df["IDENTIFIKATOR_KLIJENTA"].isin(holdout_ids)]

    feature_cols = json.loads((MODELS_DIR / "churn_feature_columns.json").read_text())
    model = pickle.load(open(MODELS_DIR / "churn_model.pkl", "rb"))

    X = feat_df.set_index("IDENTIFIKATOR_KLIJENTA")[feature_cols].copy()
    for col in X.select_dtypes("object").columns:
        X[col] = pd.Categorical(X[col])

    churn_df = pd.DataFrame(
        {
            "IDENTIFIKATOR_KLIJENTA": feat_df["IDENTIFIKATOR_KLIJENTA"].values,
            "churn_probability": model.predict_proba(X)[:, 1],
        }
    )

    merged = val_df.merge(churn_df, on="IDENTIFIKATOR_KLIJENTA", how="inner")
    return {
        row["IDENTIFIKATOR_KLIJENTA"]: {
            "value_score": float(row["value_score"]),
            "churn_probability": float(row["churn_probability"]),
        }
        for _, row in merged.iterrows()
    }


def load_scores() -> tuple[pd.DataFrame, dict[str, dict]]:
    """Load cashback scores + per-client value/risk scores."""
    df = pd.read_parquet(PROCESSED_DATA_DIR / "cashback_scores.parquet")
    df = df[df["split"] == "holdout"].copy()
    def _resolve_category(k: str) -> str | None:
        if k in _ENGLISH_CATEGORY_MAP:
            return _ENGLISH_CATEGORY_MAP[k]
        return _match_category(k, _OFFER_TOKENS)

    df["catalog_category"] = df["KATEGORIJA"].apply(_resolve_category)
    client_scores = _load_client_scores()
    return df, client_scores


def recommend(
    client_id: str,
    scores_df: pd.DataFrame,
    client_scores: dict[str, dict],
) -> list[dict] | None:
    """Return top-3 personalized cashback offers for a client, or None if not found."""
    client_rows = scores_df[scores_df["IDENTIFIKATOR_KLIJENTA"] == client_id]
    if client_rows.empty:
        return None

    scores = client_scores.get(client_id, {"value_score": 0.5, "churn_probability": 0.5})
    v_score = scores["value_score"]
    r_score = scores["churn_probability"]

    ranked = client_rows.sort_values("final_score", ascending=False)
    # Deduplicate by catalog category, keep best scoring row per category
    seen: set[str] = set()
    offers: list[dict] = []

    for row in ranked.itertuples(index=False):
        if len(offers) >= TOP_N:
            break

        catalog_cat = row.catalog_category
        if not catalog_cat or (isinstance(catalog_cat, float) and math.isnan(catalog_cat)):
            continue
        if catalog_cat in seen:
            continue

        offer_template = OFFER_BY_CATEGORY.get(catalog_cat)
        if offer_template is None:
            continue

        monthly_spend = float(row.monthly_spend)

        seen.add(catalog_cat)

        pct = calculate_dynamic_cashback(v_score, r_score, offer_template["max_percentage"] / 100)
        pct_display = round(pct * 100, 2)

        share = row.category_share_spend
        if share and not (isinstance(share, float) and math.isnan(share)) and share > 0:
            reason = f"{share * 100:.0f}% of spending in this category"
        else:
            reason = "Top ranked category by model score"

        offers.append(
            {
                "offer_id": offer_template["offer_id"],
                "category": offer_template["category"],
                "percentage": pct_display,
                "duration_months": offer_template["duration_months"],
                "min_monthly_spend": offer_template["min_monthly_spend"],
                "description": offer_template["description"],
                "reason": reason,
                "expected_monthly_cashback": round(monthly_spend * pct, 2),
            }
        )

    return offers
