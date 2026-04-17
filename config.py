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
CHURN_TX_CLIFF = 0.05          # < 5 % of avg 4-month rate → cliff
CHURN_BALANCE_COLLAPSE = 0.01  # < 1 % of avg feature-window balance → collapse

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
# Fixed z-threshold tier policy for calibrated value_score_z.
# platinum threshold set to z > 1.2816 (approximately top 10% under normality).
VALUE_TIER_LABELS = ["bronze", "silver", "gold", "platinum"]
VALUE_TIER_Z_BINS = [-float("inf"), -1.0, 0.0, 1.2816, float("inf")]

VALUE_TIERS = {
    # Normal-calibrated score ranges derived from VALUE_TIER_Z_BINS
    # with mapping: value_score = clip((value_score_z + 3) / 6, 0, 1)
    "bronze":   (0.0,      1.0 / 3.0),
    "silver":   (1.0 / 3.0, 0.5),
    "gold":     (0.5,      (1.2816 + 3.0) / 6.0),
    "platinum": ((1.2816 + 3.0) / 6.0, 1.0),
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
    "objective":        "regression",
    "n_estimators":     800,
    "num_leaves":       63,
    "learning_rate":    0.02,
    "feature_fraction": 0.8,
    "bagging_fraction": 0.8,
    "bagging_freq":     5,
    "min_child_samples": 20,
    "is_unbalance":     True,
    "verbose":          -1,
}

# ---------------------------------------------------------------------------
# ALS parameters
# ---------------------------------------------------------------------------
ALS_PARAMS = {
    "factors":        32,
    "iterations":     25,
    "regularization": 0.1,
}

# ---------------------------------------------------------------------------
# Offer catalog
# TODO (task 006): replace placeholder categories with real
# KATEGORIJA_DJELATNOSTI_DRUGE_STRANE values once known from the data
# ---------------------------------------------------------------------------
OFFER_CATALOG = [
    {
        "offer_id":          "OFF-101",
        "category":          "TRGOVINA_NA_VELIKO_I_NA_MALO",
        "max_percentage":        3.0,
        "duration_months":   3,
        "min_monthly_spend": 120,
        "description":       "3% cashback na kupnju u supermarketima i maloprodaji široke potrošnje na 3 mjeseca (min. 120 EUR/mj)",
    },
    {
        "offer_id":          "OFF-102",
        "category":          "DJELATNOSTI_PRUZANJA_SMJESTAJA_I_USLUZIVANJA_HRANE",
        "max_percentage":        5.0,
        "duration_months":   3,
        "min_monthly_spend": 80,
        "description":       "5% cashback na ugostiteljstvo i smještaj (restorani, kafići, hoteli) na 3 mjeseca (min. 80 EUR/mj)",
    },
    {
        "offer_id":          "OFF-103",
        "category":          "OPSKRBA_ELEKTRICNOM_ENERGIJOM_PLINOM_PAROM_I_KLIMATIZACIJA",
        "max_percentage":        2.0,
        "duration_months":   6,
        "min_monthly_spend": 70,
        "description":       "2% cashback na račune za struju, plin i grijanje na 6 mjeseci (min. 70 EUR/mj)",
    },
    {
        "offer_id":          "OFF-104",
        "category":          "PRIJEVOZ_I_SKLADISTENJE",
        "max_percentage":        4.0,
        "duration_months":   3,
        "min_monthly_spend": 50,
        "description":       "4% cashback na javni prijevoz, taksi i prijevozničke usluge na 3 mjeseca (min. 50 EUR/mj)",
    },
    {
        "offer_id":          "OFF-105",
        "category":          "UMJETNOST_ZABAVA_I_REKREACIJA",
        "max_percentage":        6.0,
        "duration_months":   3,
        "min_monthly_spend": 40,
        "description":       "6% cashback na kino, koncerte, sport i rekreaciju na 3 mjeseca (min. 40 EUR/mj)",
    },
    {
        "offer_id":          "OFF-106",
        "category":          "INFORMACIJE_I_KOMUNIKACIJE",
        "max_percentage":        3.0,
        "duration_months":   6,
        "min_monthly_spend": 50,
        "description":       "3% cashback na telekom usluge, streaming i druge digitalne pretplate na 6 mjeseci (min. 50 EUR/mj)",
    },
    {
        "offer_id":          "OFF-107",
        "category":          "FINANCIJSKE_DJELATNOSTI_I_OSIGURANJE",
        "max_percentage":        2.0,
        "duration_months":   3,
        "min_monthly_spend": 60,
        "description":       "2% cashback na odabrane financijske i osiguravateljske usluge (koje nisu izuzete pravilima kartičnih shema) na 3 mjeseca (min. 60 EUR/mj)",
    },
    {
        "offer_id":          "OFF-108",
        "category":          "OBRAZOVANJE",
        "max_percentage":        4.0,
        "duration_months":   6,
        "min_monthly_spend": 100,
        "description":       "4% cashback na školarine, tečajeve i online obrazovne programe na 6 mjeseci (min. 100 EUR/mj)",
    },
    {
        "offer_id":          "OFF-109",
        "category":          "OSTALE_USLUZNE_DJELATNOSTI",
        "max_percentage":        5.0,
        "duration_months":   3,
        "min_monthly_spend": 60,
        "description":       "5% cashback na usluge poput frizera, kozmetičkih salona, čišćenja i drugih osobnih usluga na 3 mjeseca (min. 60 EUR/mj)",
    },
    {
        "offer_id":          "OFF-110",
        "category":          "POLJOPRIVREDA_SUMARSTVO_I_RIBARSTVO",
        "max_percentage":        3.0,
        "duration_months":   6,
        "min_monthly_spend": 80,
        "description":       "3% cashback na kupnju u poljoprivrednim ljekarnama, trgovinama opreme i kod OPG-ova na 6 mjeseci (min. 80 EUR/mj)",
    },
    {
        "offer_id":          "OFF-111",
        "category":          "OPSKRBA_VODOM",
        "max_percentage":        1.0,
        "duration_months":   6,
        "min_monthly_spend": 50,
        "description":       "1% cashback na račune za vodu i odvodnju na 6 mjeseci (min. 50 EUR/mj)",
    },
    {
        "offer_id":          "OFF-112",
        "category":          "DJELATNOSTI_ZDRAVSTVENE_ZASTITE_I_SOCIJALNE_SKRBI",
        "max_percentage":        2.0,
        "duration_months":   3,
        "min_monthly_spend": 60,
        "description":       "2% cashback na privatne zdravstvene i socijalne usluge (ordinacije, poliklinike, domovi) na 3 mjeseca (min. 60 EUR/mj)",
    },
    {
        "offer_id":          "OFF-113",
        "category":          "STRUCNE_ZNANSTVENE_I_TEHNICKE_DJELATNOSTI",
        "max_percentage":        3.0,
        "duration_months":   3,
        "min_monthly_spend": 150,
        "description":       "3% cashback na stručne, znanstvene i tehničke usluge (konzalting, IT, pravne, računovodstvene) na 3 mjeseca (min. 150 EUR/mj)",
    },
    {
        "offer_id":          "OFF-114",
        "category":          "POSLOVANJE_NEKRETNINAMA",
        "max_percentage":        1.0,
        "duration_months":   6,
        "min_monthly_spend": 150,
        "description":       "1% cashback na odabrane transakcije povezane s poslovanjem nekretninama (agencijske naknade, upravljanje zgradama) na 6 mjeseci (min. 150 EUR/mj)",
    },
    {
        "offer_id":          "OFF-115",
        "category":          "JAVNA_UPRAVA_I_OBRANA",
        "max_percentage":        1.0,
        "duration_months":   3,
        "min_monthly_spend": 40,
        "description":       "1% cashback na plaćanja prema javnoj upravi (pristojbe, naknade) koja nisu izuzeta pravilima kartičnih shema na 3 mjeseca (min. 40 EUR/mj)",
    },
]
