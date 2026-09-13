import sys
import mlflow

from ml.components.intent.intent_preprocessor import IntentPreprocessor
from ml.components.intent.intent_trainer import IntentTrainer
from ml.components.intent.intent_evaluator import IntentEvaluator

from ml.constants.intent_constants import (
    TRAIN_FILE_PATH,
    DEV_FILE_PATH,
    TEST_FILE_PATH,
    MLFLOW_EXPERIMENT_NAME,
    MLFLOW_MODEL_NAME
)

from ml.utils.exception import MyException
from ml.utils.logger import logging


def run_intent_pipeline():

    try:

        # --------------------------------------------------
        # 1. DATA PREPROCESSING
        # --------------------------------------------------

        logging.info(
            "========== INTENT DATA PREPROCESSING =========="
        )

        preprocessor = IntentPreprocessor()

        (
            train_df,
            dev_df,
            test_df
        ) = preprocessor.load_data(
            TRAIN_FILE_PATH,
            DEV_FILE_PATH,
            TEST_FILE_PATH
        )

        logging.info(
            f"Training data shape: {train_df.shape}"
        )

        logging.info(
            f"Development data shape: {dev_df.shape}"
        )

        logging.info(
            f"Testing data shape: {test_df.shape}"
        )

        (
            X_train,
            y_train,
            X_dev,
            y_dev,
            X_test,
            y_test
        ) = preprocessor.preprocess(
            train_df,
            dev_df,
            test_df
        )

        # --------------------------------------------------
        # 2. MLFLOW EXPERIMENT
        # --------------------------------------------------

        logging.info(
            "========== MLFLOW EXPERIMENT =========="
        )

        mlflow.set_experiment(
            MLFLOW_EXPERIMENT_NAME
        )

        with mlflow.start_run():

            # --------------------------------------------------
            # 3. MODEL TRAINING
            # --------------------------------------------------

            logging.info(
                "========== MODEL TRAINING =========="
            )

            model = (
                IntentTrainer()
                .train(
                    X_train,
                    y_train
                )
            )

            # --------------------------------------------------
            # 4. MODEL EVALUATION
            # --------------------------------------------------

            logging.info(
                "========== MODEL EVALUATION =========="
            )

            metrics = (
                IntentEvaluator()
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
            # 5. DATASET INFORMATION
            # --------------------------------------------------

            logging.info(
                "========== DATASET INFORMATION =========="
            )

            mlflow.log_param(
                "num_classes",
                train_df["label"].nunique()
            )

            mlflow.log_param(
                "train_samples",
                len(train_df)
            )

            mlflow.log_param(
                "dev_samples",
                len(dev_df)
            )

            mlflow.log_param(
                "test_samples",
                len(test_df)
            )

            # --------------------------------------------------
            # 6. MODEL REGISTRATION
            # --------------------------------------------------

            logging.info(
                "========== MODEL REGISTRATION =========="
            )

            run_id = (
                mlflow.active_run()
                .info
                .run_id
            )

            model_uri = (
                f"runs:/{run_id}/intent_detection_model"
            )

            mlflow.register_model(
                model_uri,
                MLFLOW_MODEL_NAME
            )

            logging.info(
                "Intent detection model registered successfully"
            )

            # --------------------------------------------------
            # 7. PIPELINE COMPLETED
            # --------------------------------------------------

            logging.info(
                "========== INTENT PIPELINE COMPLETED =========="
            )

            return metrics

    except Exception as e:

        logging.exception(
            "Error occurred during intent detection pipeline"
        )

        raise MyException(
            e,
            sys
        ) from e


if __name__ == "__main__":

    print(
        "Starting intent detection pipeline..."
    )

    run_intent_pipeline()

    print(
        "Intent detection pipeline completed."
    )