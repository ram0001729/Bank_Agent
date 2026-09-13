import sys
import numpy as np

from ml.constants.fraud_constants import (
    TARGET_COLUMN,
    EXPECTED_COLUMNS,
    NORMAL_CLASS,
    FRAUD_CLASS,
)

from ml.utils.logger import logging
from ml.utils.exception import MyException


class DataValidation:

    def __init__(self):
        pass

    def validate_schema(self, dataframe):
        try:
            logging.info("Starting schema validation")

            actual_columns = list(dataframe.columns)

            missing_columns = [
                column
                for column in EXPECTED_COLUMNS
                if column not in actual_columns
            ]

            unexpected_columns = [
                column
                for column in actual_columns
                if column not in EXPECTED_COLUMNS
            ]

            if missing_columns:
                raise ValueError(
                    f"Missing columns: {missing_columns}"
                )

            if unexpected_columns:
                raise ValueError(
                    f"Unexpected columns: {unexpected_columns}"
                )

            if len(actual_columns) != len(EXPECTED_COLUMNS):
                raise ValueError(
                    "Dataset schema does not match expected schema"
                )

            logging.info("Schema validation successful")

            return True

        except Exception as e:
            logging.exception("Schema validation failed")
            raise MyException(e, sys) from e

    def validate_target(self, dataframe):
        try:
            logging.info("Validating target column")

            if TARGET_COLUMN not in dataframe.columns:
                raise ValueError(
                    f"Target column '{TARGET_COLUMN}' not found"
                )

            if dataframe[TARGET_COLUMN].isnull().any():
                raise ValueError(
                    "Target column contains missing values"
                )

            target_values = set(
                dataframe[TARGET_COLUMN].unique()
            )

            allowed_values = {
                NORMAL_CLASS,
                FRAUD_CLASS
            }

            invalid_values = target_values - allowed_values

            if invalid_values:
                raise ValueError(
                    f"Invalid target values: {invalid_values}"
                )

            if dataframe[TARGET_COLUMN].nunique() != 2:
                raise ValueError(
                    "Target column must contain both normal and fraud classes"
                )

            class_distribution = dataframe[
                TARGET_COLUMN
            ].value_counts()

            logging.info(
                f"Target distribution:\n{class_distribution}"
            )

            fraud_count = class_distribution.get(
                FRAUD_CLASS,
                0
            )

            if fraud_count == 0:
                raise ValueError(
                    "No fraud transactions found"
                )

            logging.info(
                f"Fraud transactions: {fraud_count}"
            )

            return True

        except Exception as e:
            logging.exception("Target validation failed")
            raise MyException(e, sys) from e

    def validate_missing_values(self, dataframe):
        try:
            logging.info("Checking missing values")

            missing_values = dataframe.isnull().sum()

            missing_values = missing_values[
                missing_values > 0
            ]

            if not missing_values.empty:
                logging.warning(
                    f"Missing values detected:\n{missing_values}"
                )
            else:
                logging.info(
                    "No missing values found"
                )

            return True

        except Exception as e:
            logging.exception(
                "Missing value validation failed"
            )
            raise MyException(e, sys) from e

    def validate_duplicates(self, dataframe):
        try:
            logging.info("Checking duplicate records")

            duplicate_count = int(
                dataframe.duplicated().sum()
            )

            duplicate_percentage = (
                duplicate_count / len(dataframe)
            ) * 100

            logging.info(
                f"Duplicate rows: {duplicate_count}"
            )

            logging.info(
                f"Duplicate percentage: "
                f"{duplicate_percentage:.4f}%"
            )

            return True

        except Exception as e:
            logging.exception(
                "Duplicate validation failed"
            )
            raise MyException(e, sys) from e

    def validate_data_types(self, dataframe):
        try:
            logging.info("Validating data types")

            numeric_columns = dataframe.select_dtypes(
                include=["number"]
            ).columns

            non_numeric_columns = [
                column
                for column in EXPECTED_COLUMNS
                if column not in numeric_columns
            ]

            if non_numeric_columns:
                raise ValueError(
                    f"Unexpected non-numeric columns: "
                    f"{non_numeric_columns}"
                )

            logging.info(
                "All dataset features are numeric"
            )

            return True

        except Exception as e:
            logging.exception(
                "Data type validation failed"
            )
            raise MyException(e, sys) from e

    def validate_numeric_values(self, dataframe):
        try:
            logging.info(
                "Checking numeric values"
            )

            numeric_data = dataframe.select_dtypes(
                include=["number"]
            )

            if np.isinf(numeric_data.to_numpy()).any():
                raise ValueError(
                    "Infinite values detected"
                )

            logging.info(
                "No infinite numeric values found"
            )

            return True

        except Exception as e:
            logging.exception(
                "Numeric value validation failed"
            )
            raise MyException(e, sys) from e

    def validate(self, dataframe):
        try:
            logging.info(
                "Starting complete data validation"
            )

            if dataframe.empty:
                raise ValueError(
                    "Dataset is empty"
                )

            self.validate_schema(
                dataframe
            )

            self.validate_target(
                dataframe
            )

            self.validate_missing_values(
                dataframe
            )

            self.validate_duplicates(
                dataframe
            )

            self.validate_data_types(
                dataframe
            )

            self.validate_numeric_values(
                dataframe
            )

            logging.info(
                "Data validation completed successfully"
            )

            return True

        except Exception as e:
            logging.exception(
                "Data validation failed"
            )
            raise MyException(e, sys) from e