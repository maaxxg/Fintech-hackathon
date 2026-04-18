# CLAUDE.md — Bank Retention, Value & Cashback Platform

## Project overview

A three-model AI platform for a bank hackathon. The system:
1. Predicts which clients are likely to churn (LightGBM binary classifier)
2. Scores each client's current value to the bank (weighted segmentation model)
3. Recommends personalized cashback offers (two-stage: ALS + LightGBM ranker)
4. Produces a merchant partnership report per value tier (aggregation + ranking)

Priority score = `churn_probability x value_score`. Focus retention budget on high-value clients at risk of churning.

## Architecture

- **Python pipeline** runs once, trains models, scores holdout clients, writes to **Firebase Firestore**.
- **SvelteKit frontend** reads from Firestore directly. Computes priority score client-side.
- **FastAPI backend** exposes one endpoint: `GET /clients/{id}/recommend`. Called on-demand from client detail page.

```
Python pipeline (runs once) --writes--> Firebase Firestore <--reads-- SvelteKit frontend
                                                                          |
                                                                          +-calls on-demand--> FastAPI /recommend
```

## Project structure

```
Fintech-hackathon/
├── CLAUDE.md
├── package.json, svelte.config.js, vite.config.ts, tsconfig.json
├── src/                                # SvelteKit frontend
│   ├── app.html, app.css, app.d.ts
│   ├── routes/
│   │   ├── +page.svelte                # Priority matrix (landing)
│   │   ├── +layout.svelte, +layout.ts
│   │   ├── client/[id]/+page.svelte    # Client detail
│   │   ├── login/+page.svelte
│   │   └── recommendations/+page.svelte
│   └── lib/
│       ├── firebase/                   # config.ts, firestore.ts, auth.ts
│       ├── api/retention.ts            # FastAPI client
│       ├── components/                 # ClientCard, ClientList, Navbar, Sidebar, etc.
│       ├── stores/                     # authStore, clientStore, themeStore
│       ├── types.ts
│       └── index.ts
├── static/                             # Logos, favicon, robots.txt
├── ML/                                 # Python ML pipeline
│   ├── requirements.txt
│   ├── config.py                       # Thresholds, paths, weights, offer catalog
│   ├── ModelToConfig.py                # Model outputs -> config format
│   ├── api/                            # FastAPI
│   │   ├── main.py
│   │   └── services/
│   ├── data/
│   │   ├── dataRaw/                    # Raw CSVs (gitignored)
│   │   ├── processed/                  # Features, splits, labels (parquet/json)
│   │   └── models/                     # Trained models (.pkl, .json)
│   │       └── CashBack/              # decision_tree, lightgbm, nmf models
│   ├── notebooks/                      # 01-07 + cashback.ipynb
│   ├── scripts/run_pipeline.sh
│   └── src/__init__.py
└── misc/                               # Planning docs (gitignored)
```

## Commands

```bash
# API (run from ML/)
cd ML && uvicorn api.main:app --reload --port 8000

# Frontend dev (run from repo root)
npm run dev

# Frontend deploy
npm run build && firebase deploy --only hosting

# Python notebooks
cd ML && jupyter notebook notebooks/

# Full pipeline
cd ML && python scripts/run_pipeline.py
```

## Tech stack

**Python:** Python 3.11+, LightGBM, SHAP, implicit (ALS), pandas, numpy, scikit-learn, firebase-admin
**API:** FastAPI + uvicorn (port 8000), Pydantic
**Frontend:** SvelteKit, Firebase JS SDK, Tailwind CSS, Chart.js/D3
**Infra:** Firebase Firestore + Hosting. No auth for hackathon.

## Data splits

70/20/10 holdout strategy. Split once with `random_state=42`. Split files saved in `ML/data/processed/split_{train,test,holdout}.json` -- never regenerate.

- **Train (70%):** fit models
- **Test (20%):** evaluate models
- **Holdout (10%):** score with trained models, write to Firestore for demo

Temporal split: feature window = [T0, T_end - 120d], outcome window = [T_end - 120d, T_end]. Never use outcome-window data for features.

## Firestore data model

**Collection `clients`** -- one doc per holdout client, doc ID = `IDENTIFIKATOR_KLIJENTA`:
```json
{
  "customer_id": "12345",
  "demographics": {
    "age": 42, "gender": "F", "education": "university",
    "marital_status": "married", "household_size": 3,
    "credit_rating": 750, "tenure_months": 87,
    "receives_primary_income_at_bank": true
  },
  "churn": {
    "score": 0.73, "tier": "act",
    "top_shap_features": [
      { "feature": "tx_count_ratio_30d_180d", "value": 0.18, "impact": 0.21 }
    ]
  },
  "value": {
    "score": 0.82, "tier": "gold",
    "components": {
      "balance_score": 0.88, "revenue_score": 0.75,
      "product_depth_score": 0.90, "tenure_score": 0.70,
      "primary_bank_score": 1.0, "credit_rating_score": 0.65
    }
  },
  "spending_profile": { "GROCERIES": 0.35, "RESTAURANTS": 0.20 },
  "summary_stats": {
    "n_products_active": 6, "total_balance_avg": 28500,
    "tx_count_total": 347, "tx_amount_total": 42800
  }
}
```

**Collection `reports`** -- single doc `merchant_partnerships`:
```json
{
  "generated_at": "2026-04-17T10:00:00Z",
  "tiers": {
    "platinum": {
      "client_count": 1200, "total_spend": 45000000,
      "top_categories": [
        { "category": "LUXURY_RETAIL", "total_spend": 5400000,
          "client_count": 890, "avg_spend_per_client": 6067,
          "tier_spend_share": 0.12, "penetration_rate": 0.74 }
      ]
    }
  }
}
```

Priority score and recommendations are NOT stored.

## FastAPI contract

**`GET /clients/{client_id}/recommend`**

Success response:
```json
{
  "customer_id": "12345",
  "recommended_offer": {
    "offer_id": "OFF-001", "category": "GROCERIES",
    "percentage": 3.0, "duration_months": 3,
    "min_monthly_spend": 100,
    "description": "3% cashback na trgovine prehrane na 3 mjeseca",
    "reason": "35% spending share in groceries",
    "expected_monthly_cashback": 15.0
  }
}
```

No eligible offers: `{ "customer_id": "12345", "recommended_offer": null, "reason": "No eligible offers" }`

Logic: read client from Firestore -> ALS top-6 candidates -> LightGBM ranker -> business rules -> first passing offer.

## Priority score fusion (computed in frontend)

```typescript
export function computePriority(churnProb: number, valueScore: number) {
    const priorityScore = churnProb * valueScore;
    let action: string;
    if (churnProb >= 0.55 && valueScore >= 0.70) action = "high_priority_retention";
    else if (churnProb >= 0.55 && valueScore < 0.40) action = "let_go";
    else if (churnProb >= 0.30 && valueScore >= 0.70) action = "monitor_high_value";
    else if (churnProb < 0.30 && valueScore >= 0.70) action = "nurture";
    else action = "no_action";
    return { priorityScore, action };
}
```

Only `high_priority_retention` clients trigger the `/recommend` API call.

## Value tiers

```python
VALUE_TIERS = { "bronze": (0.0, 0.40), "silver": (0.40, 0.70), "gold": (0.70, 0.90), "platinum": (0.90, 1.0) }
```

## Key conventions

- **Split files are sacred.** Never regenerate. Load from `ML/data/processed/split_*.json`.
- **Dates:** all UTC. T0/T_end computed from data, not hardcoded.
- **Currency:** always domestic columns (`*_U_DOMICILNOJ_VALUTI`).
- **Categories:** use `KATEGORIJA_DJELATNOSTI_DRUGE_STRANE` everywhere.
- **Feature column order:** load from JSON files, never hardcode.
- **Priority computed client-side only.** Never stored.
- **Firestore writes are one-shot.** Clear collection before re-running pipeline.
- **API is read-only.** No auth, no rate limiting, no TLS.
