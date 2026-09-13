import sys
import json
import joblib
from pathlib import Path

from ml.constants.fraud_constants import (
    TRAINED_MODEL_PATH,
    PREPROCESSOR_FILE_PATH,
    MODEL_NAME,
    MODEL_VERSION,
    MODEL_STAGE
)

from ml.utils.logger import logging
from ml.utils.exception import MyException


class ModelPusher:

    def push(
        self,
        model,
        preprocessor,
        metrics
    ):

        try:

            logging.info(
                "Starting model push"
            )

            # Create model directory
            Path(TRAINED_MODEL_PATH).parent.mkdir(
                parents=True,
                exist_ok=True
            )

            # Save trained model
            joblib.dump(
                model,
                TRAINED_MODEL_PATH
            )

            logging.info(
                f"Fraud model saved to: "
                f"{TRAINED_MODEL_PATH}"
            )

            # Create preprocessor directory
            Path(PREPROCESSOR_FILE_PATH).parent.mkdir(
                parents=True,
                exist_ok=True
            )

            # Save preprocessing pipeline
            joblib.dump(
                preprocessor,
                PREPROCESSOR_FILE_PATH
            )

            logging.info(
                f"Preprocessor saved to: "
                f"{PREPROCESSOR_FILE_PATH}"
            )

            # Save model metadata
            metadata = {
                "model_name": MODEL_NAME,
                "model_version": MODEL_VERSION,
                "model_stage": MODEL_STAGE,
                "metrics": metrics
            }

            metadata_path = (
                Path(TRAINED_MODEL_PATH).parent
                / "metadata.json"
            )

            with open(
                metadata_path,
                "w"
            ) as file:

                json.dump(
                    metadata,
                    file,
                    indent=4
                )

            logging.info(
                f"Model metadata saved to: "
                f"{metadata_path}"
            )

            logging.info(
                "Model push completed successfully"
            )

            return {
                "model_path": str(
                    TRAINED_MODEL_PATH
                ),
                "preprocessor_path": str(
                    PREPROCESSOR_FILE_PATH
                ),
                "metadata_path": str(
                    metadata_path
                )
            }

        except Exception as e:

            logging.exception(
                "Model push failed"
            )

            raise MyException(
                e,
                sys
            ) from e