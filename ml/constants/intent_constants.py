from pathlib import Path


# --------------------------------------------------
# PROJECT ROOT
# --------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[2]


# --------------------------------------------------
# BANKING77 DATASET
# --------------------------------------------------

BANKING77_DATASET_PATH = (
    PROJECT_ROOT
    / "ml"
    / "datasets"
    / "Bank_77"
)


TRAIN_FILE_PATH = (
    BANKING77_DATASET_PATH
    / "train.csv"
)

DEV_FILE_PATH = (
    BANKING77_DATASET_PATH
    / "dev.csv"
)

TEST_FILE_PATH = (
    BANKING77_DATASET_PATH
    / "test.csv"
)


# --------------------------------------------------
# DATASET COLUMNS
# --------------------------------------------------

TEXT_COLUMN = "text"

TARGET_COLUMN = "label"

LABEL_TEXT_COLUMN = "label_text"


# --------------------------------------------------
# TF-IDF CONFIGURATION
# --------------------------------------------------

NGRAM_RANGE = (1, 2)

MAX_FEATURES = 50000

SUBLINEAR_TF = True


# --------------------------------------------------
# LOGISTIC REGRESSION CONFIGURATION
# --------------------------------------------------

MAX_ITER = 1000


# --------------------------------------------------
# MLFLOW CONFIGURATION
# --------------------------------------------------

MLFLOW_EXPERIMENT_NAME = (
    "banking77_intent_detection"
)

MLFLOW_MODEL_NAME = (
    "intent_detection_model"
)