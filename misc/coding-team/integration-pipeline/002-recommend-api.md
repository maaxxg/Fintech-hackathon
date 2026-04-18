# Task 002 -- FastAPI recommend endpoint

## Context

`ML/api/main.py` has a stub `GET /clients/{client_id}/recommend` returning 501.
`ML/data/processed/cashback_scores.parquet` contains per-client, per-category rows with columns: `IDENTIFIKATOR_KLIJENTA`, `KATEGORIJA`, `split`, `final_score`, `monthly_spend`, plus others.
`ML/config.py` has `OFFER_CATALOG` (list of dicts) and path constants.

## Objective

Implement the recommend endpoint so it returns a personalized cashback offer for a given client.

## What to build

### 1. Category mapping (`ML/api/services/recommend.py`)

The parquet `KATEGORIJA` values are full Croatian names (with diacritics/encoding quirks). The `OFFER_CATALOG` uses simplified underscore keys. Build a `CATEGORY_MAP: dict[str, str]` that maps parquet category strings to catalog category strings. Only the 15 categories present in `OFFER_CATALOG` need mapping. Here are the pairs (parquet -> catalog):

| Parquet KATEGORIJA | OFFER_CATALOG category |
|---|---|
| `TRGOVINA NA VELIKO I NA MALO; POPRAVAK MOTORNIH VOZILA I MOTOCIKALA` | `TRGOVINA_NA_VELIKO_I_NA_MALO` |
| `DJELATNOSTI PRU\x8eANJA SMJE\x8aTAJA TE PRIPREME I USLU\x8eIVANJA HRANE` | `DJELATNOSTI_PRUZANJA_SMJESTAJA_I_USLUZIVANJA_HRANE` |
| `OPSKRBA ELEKTRIÈNOM ENERGIJOM, PLINOM, PAROM I KLIMATIZACIJA` | `OPSKRBA_ELEKTRICNOM_ENERGIJOM_PLINOM_PAROM_I_KLIMATIZACIJA` |
| `PRIJEVOZ I SKLADI\x8aTENJE` | `PRIJEVOZ_I_SKLADISTENJE` |
| `UMJETNOST, ZABAVA I REKREACIJA` | `UMJETNOST_ZABAVA_I_REKREACIJA` |
| `INFORMACIJE I KOMUNIKACIJE` | `INFORMACIJE_I_KOMUNIKACIJE` |
| `FINANCIJSKE DJELATNOSTI I DJELATNOSTI OSIGURANJA` | `FINANCIJSKE_DJELATNOSTI_I_OSIGURANJE` |
| `OBRAZOVANJE` | `OBRAZOVANJE` |
| `OSTALE USLU\x8eNE DJELATNOSTI` | `OSTALE_USLUZNE_DJELATNOSTI` |
| `POLJOPRIVREDA, \x8aUMARSTVO I RIBARSTVO` | `POLJOPRIVREDA_SUMARSTVO_I_RIBARSTVO` |
| `OPSKRBA VODOM; UKLANJANJE OTPADNIH VODA, GOSPODARENJE OTPADOM TE DJELATNOSTI SANACIJE OKOLI\x8aA` | `OPSKRBA_VODOM` |
| `DJELATNOSTI ZDRAVSTVENE ZA\x8aTITE I SOCIJALNE SKRBI` | `DJELATNOSTI_ZDRAVSTVENE_ZASTITE_I_SOCIJALNE_SKRBI` |
| `STRUÈNE, ZNANSTVENE I TEHNIÈKE DJELATNOSTI` | `STRUCNE_ZNANSTVENE_I_TEHNICKE_DJELATNOSTI` |
| `POSLOVANJE NEKRETNINAMA` | `POSLOVANJE_NEKRETNINAMA` |
| `JAVNA UPRAVA I OBRANA; OBVEZNO SOCIJALNO OSIGURANJE` | `JAVNA_UPRAVA_I_OBRANA` |

Important: read the actual parquet category strings at runtime to build the map keys (do not hardcode the hex escapes above -- they are shown for illustration). The simplest approach: load the parquet, get unique categories, and match each to its catalog entry. But a static dict is fine too -- just verify it works by running the API against a real client.

### 2. Recommendation service (`ML/api/services/recommend.py`)

Create a service module with:

```python
import pandas as pd
from ML.config import PROCESSED_DATA_DIR, OFFER_CATALOG

# Build offer lookup: catalog_category -> offer dict
OFFER_BY_CATEGORY = {o["category"]: o for o in OFFER_CATALOG}

def load_scores() -> pd.DataFrame:
    """Load cashback_scores.parquet, filter to holdout split, add mapped catalog category column."""
    df = pd.read_parquet(PROCESSED_DATA_DIR / "cashback_scores.parquet")
    df = df[df["split"] == "holdout"].copy()
    df["catalog_category"] = df["KATEGORIJA"].map(CATEGORY_MAP)
    return df

def recommend(client_id: str, scores_df: pd.DataFrame) -> dict:
    """Return the API response dict for a client."""
```

Logic for `recommend()`:
1. Filter `scores_df` to rows where `IDENTIFIKATOR_KLIJENTA == client_id`.
2. If no rows, return 404.
3. Sort by `final_score` descending.
4. Iterate rows. For each row where `catalog_category` is not None (i.e., has a matching offer):
   - Look up the offer in `OFFER_BY_CATEGORY`.
   - Check if `row.monthly_spend >= offer["min_monthly_spend"]`.
   - If yes, return success response with that offer. Populate:
     - `offer_id`, `category`, `duration_months`, `min_monthly_spend`, `description` from the catalog offer.
     - `percentage`: use `offer["max_percentage"]`.
     - `reason`: `f"{row.category_share_spend*100:.0f}% spending share in {row.KATEGORIJA}"` (use original category name for readability).
     - `expected_monthly_cashback`: `round(row.monthly_spend * offer["max_percentage"] / 100, 2)`.
5. If no offer passes, return `{ "customer_id": client_id, "recommended_offer": null, "reason": "No eligible offers" }`.

Note on `category_share_spend`: this column exists in the parquet. If it is NaN or 0 for the matched row, use a generic reason like `"Top ranked category by model score"`.

### 3. Wire up `ML/api/main.py`

- Add `CORSMiddleware` allowing all origins, all methods, all headers.
- On startup (`@app.on_event("startup")` or lifespan), call `load_scores()` and store the DataFrame (module-level variable or `app.state`).
- In the `/clients/{client_id}/recommend` handler, call `recommend(client_id, scores_df)` and return the result. Return 404 if client not found.
- Keep the `/health` endpoint.

### 4. Import path fix

The API is run from `ML/` with `uvicorn api.main:app`. So imports in `recommend.py` should use relative paths or `sys.path`. Simplest: in `recommend.py`, import config like:
```python
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from config import PROCESSED_DATA_DIR, OFFER_CATALOG
```
Or use relative imports if the package structure supports it. Just make sure `uvicorn api.main:app` works from `ML/`.

## Non-goals

- No auth, rate limiting, or TLS.
- No Pydantic response models (plain dicts are fine for hackathon).
- Do not modify `config.py` or `cashback_scores.parquet`.
- Do not add tests (hackathon scope).

## Acceptance criteria

- `cd ML && uvicorn api.main:app --port 8000` starts without error.
- `curl localhost:8000/health` returns `{"status":"ok"}`.
- `curl localhost:8000/clients/{valid_holdout_id}/recommend` returns a response matching the contract in CLAUDE.md.
- `curl localhost:8000/clients/NONEXISTENT/recommend` returns 404.
- CORS headers are present in responses (check with `curl -v -H "Origin: http://localhost:5173"`).
