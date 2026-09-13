import sys
import xgboost as xgb

from ml.utils.logger import logging
from ml.utils.exception import MyException

from ml.constants.fraud_constants import (
    N_ESTIMATORS,
    MAX_DEPTH,
    LEARNING_RATE,
    SUBSAMPLE,
    COLSAMPLE_BYTREE,
    MIN_CHILD_WEIGHT,
    GAMMA,
    REG_ALPHA,
    REG_LAMBDA,
    XGB_RANDOM_STATE,
    EVAL_METRIC,
)


class ModelTrainer:

    def train(
        self,
        X_train,
        y_train,
        X_valid=None,
        y_valid=None
    ):

        try:

            logging.info(
                "Starting Fraud Model Training"
            )

            negative_count = (y_train == 0).sum()
            positive_count = (y_train == 1).sum()

            if positive_count == 0:
                raise ValueError(
                    "Training data contains no fraud samples"
                )

            scale_pos_weight = (
                negative_count / positive_count
            )

            logging.info(
                f"Normal transactions: {negative_count}"
            )

            logging.info(
                f"Fraud transactions: {positive_count}"
            )

            logging.info(
                f"scale_pos_weight: {scale_pos_weight:.4f}"
            )

            model = xgb.XGBClassifier(
                n_estimators=N_ESTIMATORS,
                max_depth=MAX_DEPTH,
                learning_rate=LEARNING_RATE,
                subsample=SUBSAMPLE,
                colsample_bytree=COLSAMPLE_BYTREE,
                min_child_weight=MIN_CHILD_WEIGHT,
                gamma=GAMMA,
                reg_alpha=REG_ALPHA,
                reg_lambda=REG_LAMBDA,
                random_state=XGB_RANDOM_STATE,
                eval_metric=EVAL_METRIC,
                scale_pos_weight=scale_pos_weight,
                n_jobs=-1,
                tree_method="hist"
            )

            if X_valid is not None and y_valid is not None:

                model.fit(
                    X_train,
                    y_train,
                    eval_set=[
                        (X_valid, y_valid)
                    ],
                    verbose=False
                )

            else:

                model.fit(
                    X_train,
                    y_train
                )

            logging.info(
                "Fraud model training completed successfully"
            )

            return model

        except Exception as e:

            logging.exception(
                "Fraud model training failed"
            )

            raise MyException(
                e,
                sys
            ) from e
        