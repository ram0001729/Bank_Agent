import sys
from typing import Any

import numpy as np

from ml.utils.exception import MyException
from ml.utils.logger import logger


class FraudRiskPredictor:

    def __init__(
        self,
        model
    ):

        if model is None:
            raise ValueError(
                "Fraud model cannot be None"
            )

        self.model = model

    def predict(
        self,
        features: Any
    ) -> dict:

        try:

            prediction = self.model.predict(
                features
            )

            prediction_value = int(
                prediction[0]
            )

            probability = None

            if hasattr(
                self.model,
                "predict_proba"
            ):

                probabilities = (
                    self.model.predict_proba(
                        features
                    )
                )

                probability = float(
                    probabilities[0][1]
                )

            risk_level = (
                self._risk_level(
                    probability,
                    prediction_value
                )
            )

            logger.info(
                f"Fraud prediction="
                f"{prediction_value}, "
                f"probability={probability}, "
                f"risk={risk_level}"
            )

            return {
                "prediction": prediction_value,
                "fraud_probability": probability,
                "risk_level": risk_level,
            }

        except Exception as e:

            logger.exception(
                "Fraud risk prediction failed"
            )

            raise MyException(
                e,
                sys
            ) from e

    @staticmethod
    def _risk_level(
        probability: float | None,
        prediction: int
    ) -> str:

        if probability is None:

            return (
                "high"
                if prediction == 1
                else "low"
            )

        if probability >= 0.90:
            return "critical"

        if probability >= 0.70:
            return "high"

        if probability >= 0.40:
            return "medium"

        return "low"