# Task Brief — Score Holdout & Patch Firestore (churn + value)

## Objective

Implement `src/score_holdout.py` as a one-shot Python script that, for each of the
462 holdout clients, produces a churn probability (with top-5 SHAP features) and
attaches the already-computed value score + components, then patches the
corresponding Firestore client document under `clients/{IDENTIFIKATOR_KLIJENTA}`
with a `merge=True` write so existing demographics are preserved.

This is a prerequisite for the recommendation integration brief
(`.claude/task_brief_recommendation_integration.md`) — the frontend reads
`churn.score` and `value.score` from Firestore to drive the priority matrix and
decide whether to call `/recommend`.

> **Read the "Pending questions (verify after the Web→ML merge)" section at the
> bottom of this brief before the first run.** Several Firestore/Firebase
> details depend on the frontend branch being merged in. Most of the script
> (value loading, churn inference, SHAP, patch assembly) can be implemented
> immediately; only the init + field-name layer should be revisited after the
> merge.

## Context (what exists, what does not)

- `data/processed/split_holdout.json` — list of 462 `IDENTIFIKATOR_KLIJENTA`
  strings (12-char uppercase). Confirmed shape.
- `data/processed/features_value.parquet` — 4614 rows, columns include
  `IDENTIFIKATOR_KLIJENTA`, `value_score` (float 0–1), `value_tier`
  (`bronze`/`silver`/`gold`/`platinum`), and the 6 component scores:
  `balance_score`, `revenue_score`, `product_depth_score`, `tenure_score`,
  `primary_bank_score`, `credit_rating_score`. Note: `primary_bank_score` is
  stored as `int` (0 or 1) — cast to float before writing.
- `data/processed/features_churn.parquet` — 4614 rows × 83 columns, includes
  `IDENTIFIKATOR_KLIJENTA` plus every feature referenced in
  `data/models/churn_feature_columns.json` (82 features).
- `data/models/churn_model.pkl` — LightGBM binary classifier. Inference via
  `predict_proba(X)[:, 1]`.
- `data/models/churn_explainer.pkl` — SHAP `TreeExplainer`. Produces SHAP
  values via `explainer.shap_values(X)` (LightGBM binary returns array of
  shape `(n, n_features)` — if it returns a list of length 2, use index 1).
- `data/models/churn_feature_columns.json` — ordered list of 82 feature
  names. MUST be used to select and order columns before passing to the model.
  (Confirm this file is present after the Web→ML merge — see pending questions.)
- `src/__init__.py` — exists, empty package marker.
- `src/score_holdout.py` — **does not exist yet**, needs to be created.
- `config.py` (project root) — defines `PROCESSED_DATA_DIR` and `MODELS_DIR`.
- **Firebase init pattern:** no existing Python code in this repo initialises
  Firebase Admin at the time of writing. The only Firestore integration so far
  is on the Web branch (frontend JS SDK, project `fintech-hackathon-2`). This
  script introduces the first Python writer — see "Firebase Admin init" below
  and confirm post-merge whether a shared Python init helper has landed.

## Scope (what to do now)

Create `/Users/Max/Desktop/Fintech-hackathon/src/score_holdout.py`.

Runnable as:
```
python -m src.score_holdout
```

(From the project root. Keep imports `from config import ...` — the existing
`config.py` lives at the repo root and is imported that way elsewhere.)

### Module structure

Single file, straightforward procedural `main()` plus small helpers. No class
hierarchy.

```python
def load_holdout_ids() -> list[str]: ...
def load_value_features(holdout_ids: list[str]) -> pd.DataFrame: ...
def load_churn_features(holdout_ids: list[str]) -> pd.DataFrame: ...
def score_churn(churn_df: pd.DataFrame, feature_cols: list[str]) -> np.ndarray: ...
def compute_top_shap(explainer, X: pd.DataFrame, feature_cols: list[str],
                     k: int = 5) -> list[list[dict]]: ...
def init_firestore() -> "firestore.Client": ...
def build_patch(client_id: str,
                churn_score: float,
                top_shap: list[dict],
                value_row: pd.Series) -> dict: ...
def write_patches(db, patches: dict[str, dict]) -> None: ...
def main() -> None: ...

if __name__ == "__main__":
    main()
```

### Required behaviour — step by step

1. **Load holdout IDs** from `PROCESSED_DATA_DIR / "split_holdout.json"`.
   Expect 462 IDs. `assert len(ids) == 462` is acceptable.

2. **Load value features** from `features_value.parquet`, filter by
   `IDENTIFIKATOR_KLIJENTA.isin(holdout_ids)`. Keep only:
   `IDENTIFIKATOR_KLIJENTA`, `value_score`, `value_tier`, and the six
   components listed above. Set `IDENTIFIKATOR_KLIJENTA` as the index.

3. **Load churn features** from `features_churn.parquet`, filter to holdout
   IDs, set `IDENTIFIKATOR_KLIJENTA` as index. Do NOT reindex yet — we need
   the full frame for SHAP readable values (original dtypes preserved).

4. **Load `churn_feature_columns.json`** into `feature_cols`. Build
   `X = churn_df[feature_cols]` — this enforces column order and surfaces
   any missing column via KeyError (fail fast, acceptable).

5. **Score churn:**
   ```python
   model = joblib.load(MODELS_DIR / "churn_model.pkl")
   churn_probs = model.predict_proba(X)[:, 1]
   ```
   If loading as a `lightgbm.Booster` rather than sklearn wrapper, use
   `model.predict(X)` instead — detect at load time.

6. **Compute SHAP top-5 per client:**
   - `explainer = joblib.load(MODELS_DIR / "churn_explainer.pkl")`
   - `shap_vals = explainer.shap_values(X)` — handle both the `ndarray` and
     `list[ndarray]` return shapes: if list, take `shap_vals[1]` (positive class).
   - For each row `i`, find the indices of the top 5 features by
     `abs(shap_vals[i])`, and emit a list of 5 dicts:
     ```
     {"feature": feature_cols[j],
      "value":   <raw feature value from X.iloc[i, j], cast to python scalar>,
      "impact":  <shap_vals[i, j], cast to python float>}
     ```
   - Use native Python types (`float`, `int`, `str`). Convert `np.nan` to
     `None`. Firestore rejects `numpy.float64` in some SDK versions and
     rejects `NaN` outright.

7. **Build patch dicts.** For each holdout client ID:
   ```python
   {
     "churn": {
       "score": float(churn_prob),
       "top_shap_features": [ {feature, value, impact}, ... 5 items ... ]
     },
     "value": {
       "score": float(value_score),
       "tier":  str(value_tier),
       "components": {
         "balance_score":        float(...),
         "revenue_score":        float(...),
         "product_depth_score":  float(...),
         "tenure_score":         float(...),
         "primary_bank_score":   float(...),   # cast from int
         "credit_rating_score":  float(...),
       }
     }
   }
   ```

   (Field names / nesting must match what the frontend expects — verify
   post-merge per the pending questions section. If the frontend reads flat
   keys like `churnScore`/`valueScore`, adjust before running.)

8. **Write to Firestore with `merge=True`** so demographics already on the
   document are not clobbered. Use a `WriteBatch` with at most 500 ops per
   batch (Firestore hard limit). Commit between batches. 462 docs → 1 batch
   is enough, but implement the chunking loop anyway for robustness.

   Doc reference: `db.collection("clients").document(client_id)`.
   Write: `batch.set(ref, patch, merge=True)`.

### Firebase Admin init

No existing Python pattern to copy from at the time of writing. Implement
`init_firestore()` as a minimal standalone function:

```python
def init_firestore():
    import firebase_admin
    from firebase_admin import credentials, firestore

    if not firebase_admin._apps:
        cred_path = os.environ.get("FIREBASE_CREDENTIALS")
        if cred_path:
            cred = credentials.Certificate(cred_path)
            firebase_admin.initialize_app(cred)
        else:
            # Falls back to Application Default Credentials
            # (e.g. gcloud auth application-default login, or
            # GOOGLE_APPLICATION_CREDENTIALS env var)
            firebase_admin.initialize_app()
    return firestore.client()
```

Document in the script's module docstring that the user must either:
- set `FIREBASE_CREDENTIALS=/path/to/serviceAccount.json`, or
- set `GOOGLE_APPLICATION_CREDENTIALS=/path/to/serviceAccount.json`, or
- run `gcloud auth application-default login` beforehand.

The Firebase project is `fintech-hackathon-2` (from the frontend config on
the Web branch). ADC + the right service account key are assumed to be
provisioned by the Backend/Firestore owner (P4) before this script runs.

**After the Web→ML merge**, check whether a shared Python init helper exists
(e.g. `src/firebase_client.py`, `api/services/firebase.py`, or similar). If
it does, replace the local `init_firestore()` body with a call to that helper.
See pending questions.

### Error handling

- **Missing holdout ID in value parquet:** expected to be zero occurrences
  (value was computed for all eligible clients, holdout is a subset). If any
  appear: log a warning, skip the client (do not write a patch for that ID).
  Track count, print at end.
- **Missing holdout ID in churn parquet:** same policy — warn and skip.
- **Missing column in churn parquet that is listed in
  `churn_feature_columns.json`:** raise (fail fast). Don't paper over.
- **Firestore write failure:** let the exception propagate. No retry logic
  needed for a one-shot hackathon script.
- **NaN in SHAP top-5 `value` fields:** convert to `None` before writing.
- **NaN in churn probability:** should not happen; if it does, raise.

### Logging

Print concise progress:
- `"Loaded 462 holdout IDs"`
- `"Scored churn for N clients (mean=0.xx, min=0.xx, max=0.xx)"`
- `"Computed SHAP top-5 for N clients"`
- `"Writing N patches to Firestore..."`
- `"Done. Patched N clients. Skipped K (missing features)."`

No structured logger needed — plain `print()` is fine.

## Non-goals / Later

- Do **not** recompute the value score. It already exists in
  `features_value.parquet`. Just read and forward.
- Do **not** write the cashback recommendation or priority score — those are
  handled by the recommendation brief and the frontend respectively.
- Do **not** write the merchant partnership report (`reports/merchant_partnerships`) —
  that is Model 4's territory, separate task.
- Do **not** create Firestore docs from scratch. The 462 holdout docs already
  exist (per the prompt's stated context). This script patches; it does not
  create. (If a doc happens to be missing, `set(..., merge=True)` will create
  it — that's fine, we're not guarding against it.)
- Do **not** build a FastAPI endpoint here. This is a pipeline-time script.
- Do **not** refactor `config.py`, add a `SERVICE_ACCOUNT_PATH` constant, or
  introduce a shared Firestore helper module. YAGNI — if a second Python
  Firestore writer appears later (e.g. merchant report), extract then.

## Constraints / Caveats

- **`primary_bank_score` is `int`.** Cast to `float` before writing; mixed
  types across docs cause trouble in Firestore queries later.
- **SHAP output shape varies** by `TreeExplainer` version and model type.
  Handle both `ndarray` of shape `(n, f)` and `list` of length 2 (one array
  per class). For binary classification we want the positive class.
- **`model.predict_proba` vs `Booster.predict`:** `joblib.load` may return
  either a `lightgbm.LGBMClassifier` (sklearn API) or a raw
  `lightgbm.Booster`. Check at load time:
  ```python
  if hasattr(model, "predict_proba"):
      probs = model.predict_proba(X)[:, 1]
  else:
      probs = model.predict(X)
  ```
- **`IDENTIFIKATOR_KLIJENTA` is case-sensitive** and doubles as the Firestore
  document ID for this collection. Do not normalise case.
- **LightGBM with object dtype columns:** `features_churn.parquet` includes
  categorical string columns (e.g. `gender`, `education`). The model was
  trained with those, so passing them through should work. If LightGBM
  complains about object dtypes, cast with `pd.Categorical` per column, but
  only if needed — start simple, adjust if inference fails.
- **Firestore batch size limit is 500.** With 462 docs, a single batch works;
  still write the chunking loop for correctness and future-proofing.
- **`merge=True` is mandatory.** Overwriting would wipe the demographics
  already seeded on each client doc.

## Acceptance criteria

- `python -m src.score_holdout` runs to completion with exit code 0 from the
  project root, given valid Firebase credentials in the environment.
- End-of-run log shows `Patched 462 clients. Skipped 0.` (or, if any rows
  are genuinely missing from the feature parquets, an explicit non-zero
  skipped count with a printed list of the offending IDs).
- Spot-check in the Firebase console (or via a follow-up read) shows, for
  any 3 sampled holdout client IDs, that `clients/{id}` now contains:
  - `churn.score` as a float in `[0, 1]`
  - `churn.top_shap_features` as a 5-element array of
    `{feature, value, impact}` dicts
  - `value.score` as a float in `[0, 1]`
  - `value.tier` as one of `bronze`/`silver`/`gold`/`platinum`
  - `value.components` with all 6 component scores as floats
  - Pre-existing fields (demographics, etc.) still present (merge worked).
- Re-running the script is idempotent: produces the same output and doesn't
  corrupt existing fields.

## File map

Created:
- `/Users/Max/Desktop/Fintech-hackathon/src/score_holdout.py`

Read (not modified):
- `/Users/Max/Desktop/Fintech-hackathon/config.py`
- `/Users/Max/Desktop/Fintech-hackathon/data/processed/split_holdout.json`
- `/Users/Max/Desktop/Fintech-hackathon/data/processed/features_value.parquet`
- `/Users/Max/Desktop/Fintech-hackathon/data/processed/features_churn.parquet`
- `/Users/Max/Desktop/Fintech-hackathon/data/models/churn_model.pkl`
- `/Users/Max/Desktop/Fintech-hackathon/data/models/churn_explainer.pkl`
- `/Users/Max/Desktop/Fintech-hackathon/data/models/churn_feature_columns.json`

---

## Pending questions (verify after the Web→ML merge)

**Read this section before the first run.** These items depend on content
that lives on the `Web` (frontend) branch and will only be visible in the
`ML` branch once the merge completes. The rest of the script can be
implemented immediately against the data and models already on `ML`; only
the Firebase init and the exact field names on the patch may need small
adjustments once the merge lands.

For each item below: **do not guess.** Check the merged tree, confirm the
answer, then update the code (and, if relevant, this brief) to match.

1. **Firebase Admin init pattern used by the Web/frontend branch.**
   - Is there already a Python init helper in the merged repo (e.g.
     `src/firebase_client.py`, `src/firebase_admin_init.py`,
     `api/services/firebase.py`)? If yes, import and use it instead of the
     local `init_firestore()` defined in this brief.
   - Where does it expect the service account JSON to live? (e.g. a hardcoded
     path like `./secrets/serviceAccount.json`, or an env var name different
     from `FIREBASE_CREDENTIALS` / `GOOGLE_APPLICATION_CREDENTIALS`.)
   - Is the project ID (`fintech-hackathon-2`) passed explicitly to
     `firebase_admin.initialize_app(..., options={"projectId": ...})`, or
     inferred from the credentials?
   - Action: align this script's init with whatever pattern is canonical
     post-merge. Do not introduce a second, divergent init path.

2. **Existing shape of the holdout client documents in Firestore.**
   - Which fields are already written on each `clients/{id}` document by the
     frontend / seeding scripts on the Web branch? (demographics, spending
     profile, summary stats, anything else?)
   - Confirm the doc ID is the raw `IDENTIFIKATOR_KLIJENTA` string (and not
     a lowercased / hashed / prefixed variant).
   - Any fields whose names collide with what this script writes
     (`churn`, `value`) — if so, are they currently objects (mergeable) or
     scalars/strings (would be clobbered sub-key at a time, which is fine for
     `merge=True`, but worth knowing)?
   - Action: make sure the `merge=True` patch only writes the two top-level
     keys `churn` and `value` (plus their nested contents) and nothing else,
     so every existing field is preserved.

3. **Frontend field-name contract.**
   - CLAUDE.md specifies nested shapes (`churn.score`, `churn.top_shap_features`,
     `value.score`, `value.tier`, `value.components.*`). Confirm the merged
     frontend (`frontend/src/routes/**` and `frontend/src/lib/**`) actually
     reads these exact paths. Watch for divergences such as:
     - Flat keys: `churnScore`, `valueScore`, `valueTier`.
     - Different nesting: `scores.churn`, `scores.value`.
     - Different SHAP field names: `shap_top5` vs `top_shap_features`;
       `impact` vs `shap_value`; `feature` vs `name`.
     - Different component keys: camelCase (`balanceScore`) vs snake_case
       (`balance_score`).
   - Action: if any mismatch exists, update `build_patch()` keys before the
     first run. The frontend is the consumer of truth — change Python, not
     the frontend, unless you coordinate with P5.

4. **Presence and contents of `data/models/churn_feature_columns.json` after
   the merge.**
   - The Web branch should not touch this file, but confirm it still exists
     and is identical to the pre-merge version (82 features, matching the
     columns in `features_churn.parquet`).
   - Action: if missing, regenerate it from the training script before
     running scoring. If modified, re-diff against the model — a
     column-order mismatch silently corrupts predictions.

5. **Firestore collection/document naming.**
   - Confirm the clients collection is named exactly `clients` (plural,
     lowercase) as assumed here and in CLAUDE.md, and not something like
     `Clients`, `client`, `customers`, or nested under a parent.
   - Confirm the merchant report path `reports/merchant_partnerships` is
     what the frontend reads (not strictly needed for this script, but worth
     verifying in the same pass so later briefs don't drift).
   - Action: update the collection string in `write_patches()` if needed.

6. **`requirements.txt` coverage for `firebase-admin`.**
   - Verify the merged `requirements.txt` includes `firebase-admin` (and
     that its version resolves cleanly alongside the existing pins). If it
     was only added on the Web branch under a different dependency file
     (e.g. `api/requirements.txt`), decide which file this script's
     dependency lives in.
   - Action: add or adjust the dependency entry if missing; don't rely on it
     already being pip-installed.

7. **Any pre-existing `score_holdout.py`, `write_firestore.py`, or
   equivalent writer in the merged tree.**
   - If P4 (Backend/Firestore) already landed a writer with overlapping
     responsibilities (e.g. seeding `clients/{id}` docs), this script should
     slot in after it, not duplicate its work.
   - Action: if overlap exists, reconcile — either delete the overlap or
     narrow this script to the churn + value patch only. Flag to the
     architect before proceeding if ownership is unclear.
