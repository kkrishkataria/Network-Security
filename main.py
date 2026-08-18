from Network_Security.components.data_ingestion import DataIngestion
from Network_Security.components.data_validation import DataValidaton
from Network_Security.components.data_transformation import DataTransformation
from Network_Security.components.model_trainer import ModelTrainer
from Network_Security.exception.exception import NetworkSecurityException
from Network_Security.logging.logger import logging
from Network_Security.entity.config_entity import DataIngestionConfig,DataValidationConfig,DataTransformationConfig,ModelTrainerConfig
from Network_Security.entity.config_entity import TrainingPipelineConfig
import sys

if __name__=='__main__':
    try:
        data_ingestion=DataIngestion(DataIngestionConfig(TrainingPipelineConfig()))
        logging.info("Initiate Data Ingestion")
        data_ingestion_artifact=data_ingestion.initiate_data_ingestion()
        print(data_ingestion_artifact,'\n')
        logging.info("Data Ingestion Completed")
        data_validation=DataValidaton(data_ingestion_artifact,DataValidationConfig(TrainingPipelineConfig()))
        logging.info("Initiate Data Validation")
        data_validation_artifact=data_validation.initiate_data_validation()
        logging.info("Data Validation Completed")
        print(data_validation_artifact,'\n')
        logging.info("Initiate Data Transformation")
        data_transformation=DataTransformation(DataTransformationConfig(TrainingPipelineConfig()),data_validation_artifact)
        data_transformation_artifact=data_transformation.initiate_data_transformation()
        logging.info("Data Transformation Completed")
        print(data_transformation_artifact,'\n')
        logging.info("Initiate Model Training")
        model_training=ModelTrainer(ModelTrainerConfig(TrainingPipelineConfig()),data_transformation_artifact)
        model_training_artifact=model_training.initiate_model_trainer()
        logging.info("Model Training Completed")
        print(model_training_artifact,'\n')

        

    except Exception as e:
        raise NetworkSecurityException(e,sys)