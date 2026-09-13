import sys
import pandas as pd

from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer

from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder

from ml.utils.logger import logging
from ml.utils.exception import MyException


class DataTransformation:


    def __init__(self):
        pass


    def get_preprocessor(
        self,
        numerical_columns,
        categorical_columns
    ):

        try:

            logging.info(
                "Creating preprocessing pipeline"
            )


            # Numerical pipeline

            numerical_pipeline = Pipeline(
                steps=[

                    (
                        "imputer",
                        SimpleImputer(
                            strategy="median"
                        )
                    ),

                    (
                        "scaler",
                        StandardScaler()
                    )
                ]
            )


            # Categorical pipeline

            categorical_pipeline = Pipeline(
                steps=[

                    (
                        "imputer",
                        SimpleImputer(
                            strategy="most_frequent"
                        )
                    ),

                    (
                        "one_hot_encoder",
                        OneHotEncoder(
                            handle_unknown="ignore"
                        )
                    )

                ]
            )


            # Combine both

            preprocessor = ColumnTransformer(
                transformers=[

                    (
                        "numerical_pipeline",
                        numerical_pipeline,
                        numerical_columns
                    ),


                    (
                        "categorical_pipeline",
                        categorical_pipeline,
                        categorical_columns
                    )

                ]
            )


            return preprocessor


        except Exception as e:

            raise MyException(e,sys)



    def initiate_transformation(
            self,
            train_df,
            test_df
    ):


        try:

            logging.info(
                "Starting data transformation"
            )


            target_column = "Class"


            X_train = train_df.drop(
                target_column,
                axis=1
            )

            y_train = train_df[target_column]


            X_test = test_df.drop(
                target_column,
                axis=1
            )

            y_test = test_df[target_column]



            # Detect column types

            numerical_columns = (
                X_train
                .select_dtypes(
                    include=[
                        "int64",
                        "float64"
                    ]
                )
                .columns
                .tolist()
            )


            categorical_columns = (
                X_train
                .select_dtypes(
                    include=[
                        "object"
                    ]
                )
                .columns
                .tolist()
            )



            logging.info(
                f"Numerical columns: {numerical_columns}"
            )

            logging.info(
                f"Categorical columns: {categorical_columns}"
            )


            preprocessor = self.get_preprocessor(
                numerical_columns,
                categorical_columns
            )


            X_train_transformed = (
                preprocessor
                .fit_transform(X_train)
            )


            X_test_transformed = (
                preprocessor
                .transform(X_test)
            )


            logging.info(
                "Transformation completed"
            )


            return (
                X_train_transformed,
                X_test_transformed,
                y_train,
                y_test,
                preprocessor
            )


        except Exception as e:

            raise MyException(e,sys)