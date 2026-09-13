from ml.components.data_ingestion import DataIngestion
from ml.components.data_validation import DataValidation
from ml.components.data_eda import DataEDA
from ml.components.data_transformation import DataTransformation
from ml.components.model_trainer import ModelTrainer
from ml.components.model_evaluation import ModelEvaluation
from ml.components.model_pusher import ModelPusher

from ml.constants.fraud_constants import EDA_DIR
from ml.utils.logger import logging


def run_fraud_pipeline():

    # --------------------------------------------------
    # 1. DATA INGESTION
    # --------------------------------------------------

    logging.info("========== DATA INGESTION ==========")

    train_df, test_df = (
        DataIngestion()
        .initiate_data_ingestion()
    )


    # --------------------------------------------------
    # 2. DATA VALIDATION
    # --------------------------------------------------

    logging.info("========== DATA VALIDATION ==========")

    validator = DataValidation()

    validator.validate(train_df)
    validator.validate(test_df)


    # --------------------------------------------------
    # 3. EDA
    # --------------------------------------------------

    logging.info("========== EDA ==========")

    DataEDA(
        artifact_path=EDA_DIR
    ).initiate_eda(train_df)


    # --------------------------------------------------
    # 4. DATA TRANSFORMATION
    # --------------------------------------------------

    logging.info(
        "========== DATA TRANSFORMATION =========="
    )

    (
        X_train,
        X_test,
        y_train,
        y_test,
        preprocessor
    ) = (
        DataTransformation()
        .initiate_transformation(
            train_df,
            test_df
        )
    )


    # --------------------------------------------------
    # 5. MODEL TRAINING
    # --------------------------------------------------

    logging.info("========== MODEL TRAINING ==========")

    model = (
        ModelTrainer()
        .train(
            X_train,
            y_train
        )
    )


    # --------------------------------------------------
    # 6. MODEL EVALUATION + MLFLOW
    # --------------------------------------------------

    logging.info(
        "========== MODEL EVALUATION =========="
    )

    metrics = (
        ModelEvaluation()
        .evaluate(
            model,
            X_test,
            y_test
        )
    )


    logging.info(
        f"Final metrics: {metrics}"
    )


    # --------------------------------------------------
    # 7. MODEL PUSH
    # --------------------------------------------------

    logging.info("========== MODEL PUSH ==========")

    model_artifact = (
        ModelPusher()
        .push(
            model,
            preprocessor,
            metrics
        )
    )


    logging.info(
        f"Model artifact: {model_artifact}"
    )

    logging.info(
        "========== FRAUD PIPELINE COMPLETED =========="
    )

    return model_artifact


if __name__ == "__main__":
    run_fraud_pipeline()