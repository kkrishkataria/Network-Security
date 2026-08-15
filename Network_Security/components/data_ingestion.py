import os
import sys
import pymongo
import numpy as np
import pandas as pd

from sklearn.model_selection import train_test_split

from Network_Security.exception.exception import NetworkSecurityException
from Network_Security.logging.logger import logging
from Network_Security.entity.config_entity import DataIngestionConfig
from Network_Security.entity.artifact_entity import DataIngestionArtifact

from dotenv import load_dotenv

load_dotenv()

MONGO_DB_URL = os.getenv("MONGO_DB_URL")


class DataIngestion:

    def __init__(self, data_ingestion_config: DataIngestionConfig):
        try:
            logging.info("Initializing DataIngestion configuration")

            self.data_ingestion_config = data_ingestion_config

            logging.info("DataIngestion configuration initialized successfully")

        except Exception as e:
            logging.error("Error while initializing DataIngestion")
            raise NetworkSecurityException(e, sys)

    def export_collection_as_df(self):
        try:
            logging.info("Starting data export from MongoDB collection")

            database_name = self.data_ingestion_config.database_name
            collection_name = self.data_ingestion_config.collection_name

            logging.info(
                f"Connecting to database: {database_name}, "
                f"collection: {collection_name}"
            )

            self.mongo_client = pymongo.MongoClient(MONGO_DB_URL)

            collection = self.mongo_client[database_name][collection_name]

            logging.info("MongoDB collection reference created successfully")

            records = list(collection.find())

            logging.info(f"Successfully fetched {len(records)} records from MongoDB")

            df = pd.DataFrame(records)

            logging.info(f"DataFrame created successfully with shape: {df.shape}")

            if "_id" in df.columns:
                logging.info("Removing MongoDB _id column")
                df.drop(["_id"], axis=1, inplace=True)

            logging.info("Replacing 'na' values with NaN")

            df.replace("na", np.nan, inplace=True)

            logging.info("Data cleaning completed successfully")

            return df

        except Exception as e:
            logging.error("Error while exporting MongoDB collection as DataFrame")
            raise NetworkSecurityException(e, sys)

    def export_data_into_feature_store(self, df: pd.DataFrame):
        try:
            logging.info("Starting export of data into feature store")

            feature_store_file_path = self.data_ingestion_config.feature_store_file_path

            dir_path = os.path.dirname(feature_store_file_path)

            logging.info(f"Creating feature store directory: {dir_path}")

            os.makedirs(dir_path, exist_ok=True)

            df.to_csv(feature_store_file_path, index=False, header=False)

            logging.info(
                f"Data successfully saved to feature store: "
                f"{feature_store_file_path}"
            )

            return df

        except Exception as e:
            logging.error("Error while exporting data into feature store")
            raise NetworkSecurityException(e, sys)

    def split_data_train_test(self, df: pd.DataFrame):
        try:
            logging.info("Starting train-test data splitting")

            ratio = self.data_ingestion_config.train_test_split_ratio

            logging.info(f"Train-test split ratio: {ratio}")

            train_set, test_set = train_test_split(df, test_size=ratio)

            logging.info(f"Train set shape: {train_set.shape}")

            logging.info(f"Test set shape: {test_set.shape}")

            train_file_path = self.data_ingestion_config.training_file_path

            test_file_path = self.data_ingestion_config.testing_file_path

            dir_path = os.path.dirname(train_file_path)

            os.makedirs(dir_path, exist_ok=True)

            logging.info(f"Saving training data to: {train_file_path}")

            train_set.to_csv(train_file_path, index=False, header=True)

            logging.info(f"Saving testing data to: {test_file_path}")

            test_set.to_csv(test_file_path, index=False, header=True)

            logging.info("Train and test datasets saved successfully")

        except Exception as e:
            logging.error("Error while splitting data into train and test sets")
            raise NetworkSecurityException(e, sys)

    def initiate_data_ingestion(self):
        try:
            logging.info("========== Data Ingestion Started ==========")

            df = self.export_collection_as_df()

            logging.info("Exporting data into feature store")

            df = self.export_data_into_feature_store(df)

            logging.info("Splitting data into train and test sets")

            self.split_data_train_test(df)
            data_ingestion_artifact=DataIngestionArtifact(self.data_ingestion_config.training_file_path,self.data_ingestion_config.testing_file_path)
            logging.info("========== Data Ingestion Completed ==========")
            return data_ingestion_artifact


        except Exception as e:
            logging.error("Error occurred during data ingestion")
            raise NetworkSecurityException(e, sys)
