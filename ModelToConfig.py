from __future__ import annotations

import re
import unicodedata
from pathlib import Path
from typing import Optional

import pandas as pd
import config

# --- Hardcoded Model Parameters ---
BASE_RATE = 0.005      # B: 0.5% floor
WEIGHT_VALUE = 0.6    # wv
WEIGHT_RISK = 0.4     # wr

SCORES_PATH: Path = config.PROCESSED_DATA_DIR / "cashback_scores.parquet"

def _normalise(text: str) -> list[str]:
    """Normalise a category string into a list of comparable tokens."""
    text = text.upper()
    latin1_fixes = {
        "\xc6": "C", "\xc8": "C", "\xd0": "D", "\x8e": "Z",
        "\x9e": "Z", "\x8a": "S", "\x9a": "S", "\x90": "D",
        "Æ": "C", "È": "C", "Ð": "D",
    }
    for bad, good in latin1_fixes.items():
        text = text.replace(bad, good)

    text = "".join(
        ch for ch in unicodedata.normalize("NFKD", text)
        if unicodedata.category(ch) != "Mn"
    )
    tokens = re.split(r"[^A-Z0-9]+", text)
    return [t for t in tokens if t]

def _build_category_map(offer_catalog: list[dict]) -> dict[str, list[str]]:
    offer_tokens: dict[str, list[str]] = {}
    for offer in offer_catalog:
        cat = offer["category"]
        offer_tokens[cat] = _normalise(cat)
    return offer_tokens

def _match_category(raw_kategoria: str, offer_tokens: dict[str, list[str]]) -> Optional[str]:
    raw_toks = set(_normalise(raw_kategoria))
    best_match: Optional[str] = None
    best_score: int = 0

    for offer_cat, o_toks in offer_tokens.items():
        o_set = set(o_toks)
        overlap = len(o_set & raw_toks)
        if overlap == 0: continue
        if overlap < max(1, len(o_set) // 2): continue

        if overlap > best_score:
            best_score = overlap
            best_match = offer_cat
    return best_match

def calculate_dynamic_cashback(v_score: float, r_score: float, max_cbo: float) -> float:
    """
    Implements the Weighted Linear Model:
    Offer = B + (CBOmax - B) * (wv*v + wr*r)
    """
    # Ensure scores are normalized 0-1
    v = max(0.0, min(1.0, v_score))
    r = max(0.0, min(1.0, r_score))
    
    weighted_score = (WEIGHT_VALUE * v) + (WEIGHT_RISK * r)
    offer_value = BASE_RATE + (max_cbo - BASE_RATE) * weighted_score
    return round(offer_value, 4)

def get_ranked_offers(
    client_id: str,
    scores_path: Path = SCORES_PATH,
    top_n: Optional[int] = None,
) -> list[dict]:
    """
    Returns offers ranked by model score with dynamically calculated cashback percentages.
    """
    scores = pd.read_parquet(scores_path)
    client_scores = scores[scores["IDENTIFIKATOR_KLIJENTA"] == client_id].copy()
    
    if client_scores.empty:
        return []

    # Use the pre-calculated final_score for ranking
    client_scores = client_scores.sort_values("final_score", ascending=False)
    offer_tokens = _build_category_map(config.OFFER_CATALOG)

    client_scores["_offer_cat"] = client_scores["KATEGORIJA"].apply(
        lambda k: _match_category(k, offer_tokens)
    )

    matched = client_scores.dropna(subset=["_offer_cat"]).copy()
    matched = matched.drop_duplicates(subset=["_offer_cat"], keep="first")

    catalog_lookup: dict[str, dict] = {o["category"]: o for o in config.OFFER_CATALOG}

    ranked_offers: list[dict] = []
    for _, row in matched.iterrows():
        base_offer = catalog_lookup.get(row["_offer_cat"])
        if base_offer:
            offer = dict(base_offer)
            
            # Use max_percentage from config and the formula for specific offer percentage
            cbo_max = getattr(config, 'max_percentage', 0.03) 
            
            # Calculate dynamic rate
            # Assumes 'value_score' and 'risk_score' exist in the parquet
            v = row.get("value_score", 0.5)
            r = row.get("risk_score", 0.5)
            
            offer["percentage"] = calculate_dynamic_cashback(v, r, cbo_max)
            ranked_offers.append(offer)

    if top_n is not None:
        ranked_offers = ranked_offers[:top_n]

    return ranked_offers

if __name__ == "__main__":
    import pandas as pd
    import numpy as np

