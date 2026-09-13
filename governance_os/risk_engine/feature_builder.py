import sys

import pandas as pd

from ml.utils.exception import MyException
from ml.utils.logger import logger


class RiskFeatureBuilder:

    REQUIRED_FEATURES = [
        "amount",
    ]

    def build(
        self,
        features: dict
    ) -> pd.DataFrame:

        try:

            missing = [
                feature
                for feature
                in self.REQUIRED_FEATURES
                if feature not in features
            ]

            if missing:

                raise ValueError(
                    f"Missing fraud features: "
                    f"{missing}"
                )

            dataframe = pd.DataFrame(
                [features]
            )

            logger.debug(
                f"Risk feature vector created: "
                f"columns="
                f"{list(dataframe.columns)}"
            )

            return dataframe

        except Exception as e:

            logger.exception(
                "Risk feature construction failed"
            )

            raise MyException(
                e,
                sys
            ) from e