from pathlib import Path

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
PROJECT_ROOT = Path(__file__).parent
RAW_DATA_DIR = PROJECT_ROOT / "dataRaw"
PROCESSED_DATA_DIR = PROJECT_ROOT / "data" / "processed"
MODELS_DIR = PROJECT_ROOT / "data" / "models"

# ---------------------------------------------------------------------------
# Reproducibility
# ---------------------------------------------------------------------------
RANDOM_STATE = 42

# ---------------------------------------------------------------------------
# Data splits
# ---------------------------------------------------------------------------
SPLIT_HOLDOUT = 0.10
SPLIT_TEST = 2 / 9

# ---------------------------------------------------------------------------
# Temporal windows
# ---------------------------------------------------------------------------
OUTCOME_WINDOW_DAYS = 120

# ---------------------------------------------------------------------------
# Churn label thresholds
# ---------------------------------------------------------------------------
CHURN_TX_CLIFF = 0.15
CHURN_BALANCE_COLLAPSE = 0.05

# ---------------------------------------------------------------------------
# Inclusion threshold
# ---------------------------------------------------------------------------
MIN_TX_FEATURE_WINDOW = 10

# ---------------------------------------------------------------------------
# Value score weights and tiers
# ---------------------------------------------------------------------------
VALUE_WEIGHTS = {
    "balance_score":        0.30,
    "revenue_score":        0.25,
    "product_depth_score":  0.20,
    "tenure_score":         0.10,
    "primary_bank_score":   0.10,
    "credit_rating_score":  0.05,
}

VALUE_TIERS = {
    "bronze":   (0.0,  0.40),
    "silver":   (0.40, 0.70),
    "gold":     (0.70, 0.90),
    "platinum": (0.90, 1.0),
}

# ---------------------------------------------------------------------------
# LightGBM churn model hyperparameters
# ---------------------------------------------------------------------------
CHURN_PARAMS = {
    "objective":        "binary",
    "n_estimators":     500,
    "num_leaves":       63,
    "learning_rate":    0.03,
    "feature_fraction": 0.8,
    "bagging_fraction": 0.8,
    "bagging_freq":     5,
    "is_unbalance":     True,
    "min_data_in_leaf": 50,
    "verbose":          -1,
}

# ---------------------------------------------------------------------------
# LightGBM ranker hyperparameters
# ---------------------------------------------------------------------------
RANKER_PARAMS = {
    "objective":        "binary",
    "n_estimators":     200,
    "num_leaves":       31,
    "learning_rate":    0.05,
    "feature_fraction": 0.8,
    "is_unbalance":     True,
    "verbose":          -1,
}

# ---------------------------------------------------------------------------
# ALS parameters
# ---------------------------------------------------------------------------
ALS_PARAMS = {
    "factors":        24,
    "iterations":     20,
    "regularization": 0.1,
}

# ---------------------------------------------------------------------------
# Offer catalog
# TODO (task 006): replace placeholder categories with real
# KATEGORIJA_DJELATNOSTI_DRUGE_STRANE values once known from the data
# ---------------------------------------------------------------------------
OFFER_CATALOG = [
    {
        "offer_id":          "OFF-001",
        "category":          "MALOPRODAJA_PREHRAMBENIH_ARTIKALA",
        "percentage":        3.0,
        "duration_months":   3,
        "min_monthly_spend": 100,
        "description":       "3% cashback na maloprodaju prehrambenih artikala na 3 mjeseca",
    },
    {
        "offer_id":          "OFF-002",
        "category":          "UGOSTITELJSTVO",
        "percentage":        5.0,
        "duration_months":   3,
        "min_monthly_spend": 50,
        "description":       "5% cashback na ugostiteljske usluge na 3 mjeseca",
    },
    {
        "offer_id":          "OFF-003",
        "category":          "GORIVO",
        "percentage":        4.0,
        "duration_months":   6,
        "min_monthly_spend": 80,
        "description":       "4% cashback na gorivo na 6 mjeseci",
    },
    {
        "offer_id":          "OFF-004",
        "category":          "ZABAVA",
        "percentage":        6.0,
        "duration_months":   3,
        "min_monthly_spend": 40,
        "description":       "6% cashback na zabavu i rekreaciju na 3 mjeseca",
    },
]
