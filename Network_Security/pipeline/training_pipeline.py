import os,sys
from Network_Security.logging.logger import logging
from Network_Security.exception.exception import NetworkSecurityException

from Network_Security.components.data_ingestion import DataIngestion
from Network_Security.components.data_transformation import DataTransformation
from Network_Security.components.data_validation import DataValidaton
from Network_Security.components.model_trainer import ModelTrainer
from Network_Security.entity.config_entity import ModelTrainerConfig,DataIngestionConfig,DataValidationConfig,TrainingPipelineConfig,DataTransformationConfig

from Network_Security.entity.artifact_entity import DataIngestionArtifact,DataTransformationArtifact,DataValidationArtifact,ModelTrainerArtifact

class TrainingPipeline:
    def __init__(self):
        self.training_pipeline_config=TrainingPipelineConfig()

    def start_data_ingestion(self):
        try:
            self.data_ingestion_config=DataIngestionConfig(self.training_pipeline_config)
            logging.info("Start Data Ingestion")
            data_ingestion=DataIngestion(self.data_ingestion_config)
            data_ingestion_artifact:DataIngestionArtifact=data_ingestion.initiate_data_ingestion()
            logging.info(f"Data Ingestion Completed and artifact {data_ingestion_artifact}")
            return data_ingestion_artifact
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def start_data_validation(self,data_ingestion_artifact:DataIngestionArtifact):
        try:
            self.data_validation_config=DataValidationConfig(self.training_pipeline_config)
            logging.info("Start Data Validation")
            data_validation=DataValidaton(data_ingestion_artifact,self.data_validation_config)
            data_validation_artifact:DataValidationArtifact=data_validation.initiate_data_validation()
            logging.info(f"Data Validation Completed and artifact {data_validation_artifact}")
            return data_validation_artifact
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        

    def start_data_transformation(
        self,
        data_validation_artifact: DataValidationArtifact
    ):
        try:
            # Create CONFIG
            self.data_transformation_config = DataTransformationConfig(
                self.training_pipeline_config
            )

            logging.info("Start Data transformation")

            # Create COMPONENT
            data_transformation = DataTransformation(
                self.data_transformation_config,
                data_validation_artifact
            )

            # Run transformation
            data_transformation_artifact: DataTransformationArtifact = (
                data_transformation.initiate_data_transformation()
            )

            logging.info(
                f"Data transformation Completed and artifact "
                f"{data_transformation_artifact}"
            )

            return data_transformation_artifact

        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def start_model_trainer(self,data_transformation_artifact:DataTransformationArtifact):
        try:
            self.model_trainer_config=ModelTrainerConfig(self.training_pipeline_config)
            logging.info("Start Model Training")
            model_trainer=ModelTrainer(self.model_trainer_config,data_transformation_artifact)
            model_trainer_artifact:ModelTrainerArtifact=model_trainer.initiate_model_trainer()
            logging.info(f"Model Training Completed and artifact {model_trainer_artifact}")
            return model_trainer_artifact
        except Exception as e:
            raise NetworkSecurityException(e,sys)

    def run_pipeline(self):
        try:
            data_ingestion_artifact=self.start_data_ingestion()
            data_validation_artifact=self.start_data_validation(data_ingestion_artifact)
            data_transformation_artifact=self.start_data_transformation(data_validation_artifact)
            model_trainer_artifact=self.start_model_trainer(data_transformation_artifact)
            return model_trainer_artifact
        except Exception as e:
            raise NetworkSecurityException(e,sys)