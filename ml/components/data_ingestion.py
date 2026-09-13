import sys
from pathlib import Path

import pandas as pd
from sklearn.model_selection import train_test_split

from ml.constants.fraud_constants import (
    FRAUD_DATASET_PATH,
    FEATURE_STORE_PATH,
    TRAIN_FILE_PATH,
    TEST_FILE_PATH,
    TRAIN_TEST_SPLIT_RATIO,
    RANDOM_STATE,
    TARGET_COLUMN,
)

from ml.utils.exception import MyException
from ml.utils.logger import logging


class DataIngestion:

    def initiate_data_ingestion(self):

        try:

            logging.info("Starting data ingestion")

            # Load dataset
            df = pd.read_csv(FRAUD_DATASET_PATH)

            logging.info(
                f"Dataset shape: {df.shape}"
            )

            # Validate target column exists
            if TARGET_COLUMN not in df.columns:
                raise ValueError(
                    f"Target column '{TARGET_COLUMN}' not found"
                )

            # Create artifact directories
            Path(FEATURE_STORE_PATH).parent.mkdir(
                parents=True,
                exist_ok=True
            )

            Path(TRAIN_FILE_PATH).parent.mkdir(
                parents=True,
                exist_ok=True
            )

            Path(TEST_FILE_PATH).parent.mkdir(
                parents=True,
                exist_ok=True
            )

            # Save feature store
            df.to_csv(
                FEATURE_STORE_PATH,
                index=False
            )

            logging.info(
                f"Feature store saved to: {FEATURE_STORE_PATH}"
            )

            # Train-test split
            train_df, test_df = train_test_split(
                df,
                test_size=TRAIN_TEST_SPLIT_RATIO,
                random_state=RANDOM_STATE,
                stratify=df[TARGET_COLUMN]
            )

            # Save train/test datasets
            train_df.to_csv(
                TRAIN_FILE_PATH,
                index=False
            )

            test_df.to_csv(
                TEST_FILE_PATH,
                index=False
            )

            logging.info(
                f"Training data shape: {train_df.shape}"
            )

            logging.info(
                f"Testing data shape: {test_df.shape}"
            )

            logging.info(
                "Data ingestion completed successfully"
            )

            return train_df, test_df

        except Exception as e:

            logging.exception(
                "Error occurred during data ingestion"
            )

            raise MyException(e, sys) from e