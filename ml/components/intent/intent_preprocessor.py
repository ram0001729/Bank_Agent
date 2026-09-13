import re
import sys

from ml.utils.exception import MyException
from ml.utils.logger import logging


class IntentPreprocessor:

    def clean_text(self, text):

        try:

            text = str(text)

            text = text.strip()

            text = re.sub(
                r"\s+",
                " ",
                text
            )

            text = re.sub(
                r"[^\w\s']",
                "",
                text
            )

            text = text.lower()

            return text

        except Exception as e:

            logging.exception(
                "Error occurred during text cleaning"
            )

            raise MyException(e, sys) from e

    def preprocess(
        self,
        train_df,
        dev_df,
        test_df
    ):

        try:

            logging.info(
                "Starting intent text preprocessing"
            )

            train_df = train_df.copy()
            dev_df = dev_df.copy()
            test_df = test_df.copy()

            train_df["text"] = (
                train_df["text"]
                .fillna("")
                .apply(self.clean_text)
            )

            dev_df["text"] = (
                dev_df["text"]
                .fillna("")
                .apply(self.clean_text)
            )

            test_df["text"] = (
                test_df["text"]
                .fillna("")
                .apply(self.clean_text)
            )

            X_train = train_df["text"]
            y_train = train_df["label"]

            X_dev = dev_df["text"]
            y_dev = dev_df["label"]

            X_test = test_df["text"]
            y_test = test_df["label"]

            logging.info(
                "Intent text preprocessing completed"
            )

            return (
                X_train,
                y_train,
                X_dev,
                y_dev,
                X_test,
                y_test
            )

        except Exception as e:

            logging.exception(
                "Error occurred during intent preprocessing"
            )

            raise MyException(e, sys) from e