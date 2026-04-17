"""
offer_recommender.py
--------------------
Maps model scores (cashback_scores.parquet) to concrete offers from OFFER_CATALOG
and returns them ranked by predicted benefit for a given client.

Usage
-----
    from offer_recommender import get_ranked_offers

    offers = get_ranked_offers("U8BT04CPPO69")
    for o in offers:
        print(o)

The function returns a list of offer dicts (same structure as OFFER_CATALOG),
ordered from highest to lowest predicted benefit.  Only offers whose category
has a score in the model output are returned.  If the client is not found in
the scores file, an empty list is returned.
"""

from __future__ import annotations

import re
import unicodedata
from pathlib import Path
from typing import Optional

import pandas as pd

# ---------------------------------------------------------------------------
# Import project config (assumes this script lives next to config.py, or that
# the project root is on sys.path).
# ---------------------------------------------------------------------------
import config

# ---------------------------------------------------------------------------
# Path to the pre-computed scores produced by cashback.ipynb
# ---------------------------------------------------------------------------
SCORES_PATH: Path = config.PROCESSED_DATA_DIR / "cashback_scores.parquet"


# ---------------------------------------------------------------------------
# Category normalisation
# ---------------------------------------------------------------------------
# The model uses KATEGORIJA strings from raw transactions (e.g.
# "TRGOVINA NA VELIKO I NA MALO; POPRAVAK MOTORNIH VOZILA I MOTOCIKALA").
# OFFER_CATALOG uses simplified underscore keys (e.g.
# "TRGOVINA_NA_VELIKO_I_NA_MALO").
#
# Strategy: normalise both sides to a common token set and match on the
# longest common leading token run, then fall back to substring containment.

def _normalise(text: str) -> list[str]:
    """
    Normalise a category string into a list of comparable tokens.

    Steps:
    1. Uppercase.
    2. Fix Latin-1 mis-decodes of Croatian letters that appear as control/box
       characters (e.g. Æ→C, Š→S, Ž→Z, Đ→D) — these occur when UTF-8 text
       is read as Latin-1 by the CSV parser.
    3. Apply Unicode NFKD decomposition and strip all combining diacritic marks
       (category Mn).  This handles properly-encoded Croatian letters
       (Č, Ć, Š, Ž, Đ → C, C, S, Z, D) regardless of source encoding.
    4. Split on anything that is not A-Z or 0-9 (underscores, spaces,
       semicolons, commas, hyphens all become delimiters).
    5. Drop empty tokens.
    """
    text = text.upper()

    # --- Step 2: fix common Latin-1 garbling of Croatian letters ---
    latin1_fixes = {
        # garbled form : correct ASCII base
        "\xc6": "C",  # Æ  (mis-decoded Č or Ć)
        "\xc8": "C",  # È  (mis-decoded Č)
        "\xd0": "D",  # Ð  (mis-decoded Đ)
        "\x8e": "Z",  # Ž  (Windows-1250 code point leaked through)
        "\x9e": "Z",
        "\x8a": "S",  # Š
        "\x9a": "S",
        "\x90": "D",  # Đ  (Windows-1250)
        "Æ": "C", "È": "C",
        "Ð": "D",
    }
    for bad, good in latin1_fixes.items():
        text = text.replace(bad, good)

    # --- Step 3: Unicode decomposition + strip combining marks ---
    # NFKD splits e.g. Č → C + ̌  (combining caron), then we drop all Mn chars.
    text = "".join(
        ch for ch in unicodedata.normalize("NFKD", text)
        if unicodedata.category(ch) != "Mn"
    )

    # --- Step 4 & 5: tokenise ---
    tokens = re.split(r"[^A-Z0-9]+", text)
    return [t for t in tokens if t]


def _build_category_map(offer_catalog: list[dict]) -> dict[str, str]:
    """
    Returns a mapping:
        offer_category_key  →  offer_category_key   (identity, already normalised)

    We build it so we can look up raw KATEGORIJA strings and find the best
    matching offer category.
    """
    # Pre-tokenise offer categories
    offer_tokens: dict[str, list[str]] = {}
    for offer in offer_catalog:
        cat = offer["category"]
        offer_tokens[cat] = _normalise(cat)
    return offer_tokens


def _match_category(raw_kategoria: str, offer_tokens: dict[str, list[str]]) -> Optional[str]:
    """
    Try to find the best matching offer category for a raw KATEGORIJA string.

    Strategy (in priority order):
    1. Exact match after normalising punctuation/case.
    2. All offer tokens appear in the raw category tokens.
    3. First N tokens of the offer category match the first N tokens of raw.
    4. Fallback: offer tokens that are a subset of raw tokens (partial match).
    """
    raw_toks = set(_normalise(raw_kategoria))

    best_match: Optional[str] = None
    best_score: int = 0

    for offer_cat, o_toks in offer_tokens.items():
        o_set = set(o_toks)

        # Score = number of offer tokens found in raw tokens
        overlap = len(o_set & raw_toks)
        if overlap == 0:
            continue

        # Require at least half the offer tokens to match
        if overlap < max(1, len(o_set) // 2):
            continue

        if overlap > best_score:
            best_score = overlap
            best_match = offer_cat

    return best_match


# ---------------------------------------------------------------------------
# Main public function
# ---------------------------------------------------------------------------

def get_ranked_offers(
    client_id: str,
    scores_path: Path = SCORES_PATH,
    top_n: Optional[int] = None,
) -> list[dict]:
    """
    Return OFFER_CATALOG offers ranked by model score for ``client_id``.

    Parameters
    ----------
    client_id   : Client identifier (IDENTIFIKATOR_KLIJENTA).
    scores_path : Path to cashback_scores.parquet (default: from config).
    top_n       : If set, return only the top N offers.

    Returns
    -------
    List of offer dicts from OFFER_CATALOG, ordered best → worst predicted
    benefit.  Each dict contains: offer_id, category, percentage,
    duration_months, min_monthly_spend, description.
    """
    # --- Load scores ---
    scores = pd.read_parquet(scores_path)

    # Filter to this client
    client_scores = scores[scores["IDENTIFIKATOR_KLIJENTA"] == client_id].copy()
    if client_scores.empty:
        return []

    # Sort descending by final_score
    client_scores = client_scores.sort_values("final_score", ascending=False)

    # --- Build offer lookup ---
    offer_tokens = _build_category_map(config.OFFER_CATALOG)

    # Map each scored KATEGORIJA to an offer category
    client_scores["_offer_cat"] = client_scores["KATEGORIJA"].apply(
        lambda k: _match_category(k, offer_tokens)
    )

    # Drop rows that didn't match any offer
    matched = client_scores.dropna(subset=["_offer_cat"]).copy()

    # Keep only the best-scoring row per offer category (in case multiple
    # raw categories map to the same offer)
    matched = matched.drop_duplicates(subset=["_offer_cat"], keep="first")

    # Build offer_cat → offer dict lookup
    catalog_lookup: dict[str, dict] = {o["category"]: o for o in config.OFFER_CATALOG}

    # Assemble final ranked list
    ranked_offers: list[dict] = []
    for _, row in matched.iterrows():
        offer = catalog_lookup.get(row["_offer_cat"])
        if offer is not None:
            ranked_offers.append(dict(offer))  # return a copy

    if top_n is not None:
        ranked_offers = ranked_offers[:top_n]

    return ranked_offers


# ---------------------------------------------------------------------------
# CLI / quick test
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    import sys
    import json

    if len(sys.argv) < 2:
        print("Usage: python offer_recommender.py <CLIENT_ID> [top_n]")
        sys.exit(1)

    cid = sys.argv[1]
    n   = int(sys.argv[2]) if len(sys.argv) > 2 else None

    results = get_ranked_offers(cid, top_n=n)

    if not results:
        print(f"No offers found for client '{cid}'.")
    else:
        print(f"Ranked offers for client '{cid}' ({len(results)} total):\n")
        print(json.dumps(results, ensure_ascii=False, indent=2))