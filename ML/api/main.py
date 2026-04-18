import logging
import pandas as pd
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from api.services.recommend import load_scores, recommend as _recommend

app = FastAPI(title="Bank Retention API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

_scores_df: pd.DataFrame | None = None
_client_scores: dict | None = None


@app.on_event("startup")
def startup_event() -> None:
    global _scores_df, _client_scores
    try:
        _scores_df, _client_scores = load_scores()
    except Exception as exc:
        logging.getLogger(__name__).error("Failed to load scores: %s", exc)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/clients/{client_id}/recommend")
def recommend(client_id: str):
    if _scores_df is None or _client_scores is None:
        raise HTTPException(status_code=503, detail="Service not ready")

    result = _recommend(client_id, _scores_df, _client_scores)
    if result is None:
        raise HTTPException(status_code=404, detail=f"Client '{client_id}' not found")

    return {"customer_id": client_id, "offers": result}
