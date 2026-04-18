# Task 001: Score holdout clients and write to Firestore

## Context

The frontend reads from Firestore collection `clients`. Each doc must have flat fields matching the TypeScript `Client` interface:
```
id, managerId, name, riskScore (0-100 int), valueScore (0-100 int),
riskExplanation, valueExplanation, email, phone, accountType, joinDate
```

The `[key: string]: any` catch-all in the interface means extra fields (demographics, spending, SHAP, etc.) will render in the "Extended Profile" section of the client detail page.

## Objective

Create `ML/scripts/score_holdout.py` that:
1. Loads holdout client IDs from `ML/data/processed/split_holdout.json`
2. Scores them with the churn model + SHAP explainer
3. Reads their value scores from `features_value.parquet`
4. Reads their spending profile from `cashback_scores.parquet`
5. Writes one Firestore doc per client to collection `clients`

## File to create

`ML/scripts/score_holdout.py`

## Implementation details

### Firebase init
```python
import os
from firebase_admin import credentials, firestore, initialize_app

key_path = os.environ.get(
    "GOOGLE_APPLICATION_CREDENTIALS",
    os.path.join(os.path.dirname(__file__), "..", "..", "fintech-hackathon-2-firebase-adminsdk-fbsvc-5e5a462a40.json")
)
cred = credentials.Certificate(key_path)
initialize_app(cred)
db = firestore.client()
```

### Churn scoring
- Load `ML/data/models/churn_model.pkl` (LGBMClassifier), `ML/data/models/churn_explainer.pkl` (SHAP TreeExplainer), `ML/data/models/churn_feature_columns.json`
- Load `ML/data/processed/features_churn.parquet`, filter to holdout IDs
- Extract feature matrix using the column order from `churn_feature_columns.json`
- `churn_prob = model.predict_proba(X)[:, 1]`
- SHAP: `shap_values = explainer.shap_values(X)` -- for binary classifier this returns a list of 2 arrays; use index [1]. Get top 3 features per client by absolute SHAP value.

### Value scoring
- Load `ML/data/processed/features_value.parquet`, filter to holdout IDs
- `value_score` is already in [0, 1]. Also grab `value_tier` and the 6 component scores.

### Spending profile
- Load `ML/data/processed/cashback_scores.parquet`, filter to holdout IDs
- Group by client, pivot on `KATEGORIJA`, use `monthly_spend` as value
- Result: dict of {category: monthly_spend} per client (only categories with monthly_spend > 0)

### Firestore doc structure (flat, matching Client interface)

For each holdout client, write/merge to `clients/{IDENTIFIKATOR_KLIJENTA}`:

```python
doc = {
    # Required by Client interface
    "managerId": "demo-manager",  # fixed value for hackathon
    "name": f"Klijent {client_id[:6]}",
    "riskScore": int(round(churn_prob * 100)),  # 0-100 int
    "valueScore": int(round(value_score * 100)),  # 0-100 int
    "riskExplanation": f"Top churn drivers: {top_shap_features_text}",
    "valueExplanation": f"{value_tier.capitalize()} tier client (score: {value_score:.2f})",
    "email": f"klijent.{client_id[:6].lower()}@banka.hr",
    "phone": f"+385 91 {random_7_digits}",
    "accountType": value_tier.capitalize(),  # "Bronze" / "Silver" / "Gold" / "Platinum"
    "joinDate": join_date_str,  # derive from tenure_months in features_value

    # Extra fields (will appear in Extended Profile)
    "churn_probability": round(churn_prob, 4),
    "value_score_raw": round(value_score, 4),
    "value_tier": value_tier,
    "spending_profile": spending_dict,  # {category: monthly_spend}
    "shap_top3": [{"feature": name, "impact": round(val, 4)} for ...],
    "balance_score": round(bs, 4),
    "revenue_score": round(rs, 4),
    "product_depth_score": round(pds, 4),
    "tenure_score": round(ts, 4),
    "primary_bank_score": round(pbs, 4),
    "credit_rating_score": round(crs, 4),
}
```

### riskExplanation generation
Format top 3 SHAP features as: `"Top churn drivers: tx_count_ratio_30d_180d (+0.21), balance_trend_slope (-0.15), days_since_last_tx (+0.12)"`
Use the sign of the SHAP value (+ means pushes toward churn).

### joinDate generation
`tenure_months` is in `features_value.parquet`. Compute: `datetime(2026, 4, 17) - timedelta(days=tenure_months * 30.44)`, format as `"YYYY-MM-DD"`.

### Phone number generation
Use `random.seed(42)` at top. For each client: `random.randint(1000000, 9999999)`.

### Write strategy
- Use `db.collection("clients").document(client_id).set(doc)` (overwrite entire doc)
- Batch writes in groups of 500 (Firestore batch limit)
- Print progress every 100 clients

### Error handling
- If a holdout ID is missing from features_churn or features_value, skip it and log a warning
- Print summary at end: "Wrote N docs to Firestore"

## Non-goals
- Do NOT generate the merchant_partnerships report doc
- Do NOT implement the /recommend endpoint
- Do NOT modify any frontend files
- Do NOT create any new parquet files

## Constraints
- All paths relative to `ML/` directory using `pathlib` and `config.py` constants (`PROCESSED_DATA_DIR`, `MODELS_DIR`)
- Import and use `sys.path` to add project root so `config` module is importable
- The script must be runnable as `cd ML && python scripts/score_holdout.py`
