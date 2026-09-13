from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]

ML_DIR = PROJECT_ROOT / "ml"
DATASET_DIR = ML_DIR / "datasets"
ARTIFACT_DIR = ML_DIR / "artifacts"
MODEL_DIR = ML_DIR / "models"


# Dataset
FRAUD_DATASET_PATH = (
    DATASET_DIR / "creditcard.csv"
)


# Target / schema
TARGET_COLUMN = "Class"

NORMAL_CLASS = 0
FRAUD_CLASS = 1

EXPECTED_COLUMNS = [
    "Time",
    "V1", "V2", "V3", "V4", "V5",
    "V6", "V7", "V8", "V9", "V10",
    "V11", "V12", "V13", "V14", "V15",
    "V16", "V17", "V18", "V19", "V20",
    "V21", "V22", "V23", "V24", "V25",
    "V26", "V27", "V28",
    "Amount",
    "Class",
]


# Data ingestion
DATA_INGESTION_DIR = ARTIFACT_DIR / "fraud" / "data_ingestion"

FEATURE_STORE_PATH = (
    DATA_INGESTION_DIR / "feature_store.csv"
)

TRAIN_FILE_PATH = (
    DATA_INGESTION_DIR / "train.csv"
)

TEST_FILE_PATH = (
    DATA_INGESTION_DIR / "test.csv"
)

TRAIN_TEST_SPLIT_RATIO = 0.20
RANDOM_STATE = 42


# EDA
EDA_DIR = ARTIFACT_DIR / "fraud" / "eda"


# Transformation
DATA_TRANSFORMATION_DIR = (
    ARTIFACT_DIR / "fraud" / "data_transformation"
)

PREPROCESSOR_FILE_PATH = (
    DATA_TRANSFORMATION_DIR / "preprocessor.pkl"
)


# Model
TRAINED_MODEL_PATH = (
    MODEL_DIR / "fraud_detection" / "fraud_model.pkl"
)

N_ESTIMATORS = 300
MAX_DEPTH = 6
LEARNING_RATE = 0.05
SUBSAMPLE = 0.8
COLSAMPLE_BYTREE = 0.8
MIN_CHILD_WEIGHT = 1
GAMMA = 0
REG_ALPHA = 0
REG_LAMBDA = 1

XGB_RANDOM_STATE = 42
EVAL_METRIC = "logloss"


# Evaluation
MODEL_EVALUATION_DIR = (
    ARTIFACT_DIR / "fraud" / "model_evaluation"
)

METRICS_PATH = (
    MODEL_EVALUATION_DIR / "metrics.json"
)

CONFUSION_MATRIX_FILE_NAME = "confusion_matrix.png"

MIN_RECALL = 0.70
MIN_PRECISION = 0.50
MIN_F1_SCORE = 0.60
MIN_ROC_AUC = 0.60
MIN_PR_AUC = 0.60


# MLflow
MLFLOW_EXPERIMENT_NAME = "fraud_detection"
MLFLOW_MODEL_NAME = "fraud_detection_model"


# Model version
MODEL_NAME = "fraud_detection_model"
MODEL_VERSION = "v1"
MODEL_STAGE = "staging"