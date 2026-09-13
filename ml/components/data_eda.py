import os
import sys
import json

import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns

from ml.utils.logger import logging
from ml.utils.exception import MyException



class DataEDA:


    def __init__(self, artifact_path):

        self.artifact_path = artifact_path


        os.makedirs(
            self.artifact_path,
            exist_ok=True
        )



    def generate_dataset_report(self, df):

        try:

            logging.info(
                "Starting EDA"
            )


            report = {

                "rows":
                df.shape[0],


                "columns":
                df.shape[1],


                "missing_values":
                df.isnull().sum().to_dict(),


                "duplicate_rows":
                int(df.duplicated().sum()),


                "class_distribution":
                df["Class"].value_counts().to_dict()

            }


            with open(
                os.path.join(
                    self.artifact_path,
                    "dataset_report.json"
                ),
                "w"
            ) as file:

                json.dump(
                    report,
                    file,
                    indent=4
                )


            logging.info(
                "EDA report generated"
            )


        except Exception as e:

            raise MyException(e,sys)



    def plot_class_distribution(self,df):

        try:

            plt.figure(
                figsize=(6,4)
            )


            sns.countplot(
                x="Class",
                data=df
            )


            plt.title(
                "Fraud Distribution"
            )


            plt.savefig(
                os.path.join(
                    self.artifact_path,
                    "class_distribution.png"
                )
            )


            plt.close()


        except Exception as e:

            raise MyException(e,sys)



    def plot_correlation(self,df):

        try:

            plt.figure(
                figsize=(15,10)
            )


            sns.heatmap(
                df.corr(),
                cmap="coolwarm"
            )


            plt.title(
                "Feature Correlation"
            )


            plt.savefig(
                os.path.join(
                    self.artifact_path,
                    "correlation_heatmap.png"
                )
            )


            plt.close()


        except Exception as e:

            raise MyException(e,sys)



    def initiate_eda(self,df):

        logging.info(
            "Running EDA pipeline"
        )


        self.generate_dataset_report(df)

        self.plot_class_distribution(df)

        self.plot_correlation(df)


        logging.info(
            "EDA completed successfully"
        )