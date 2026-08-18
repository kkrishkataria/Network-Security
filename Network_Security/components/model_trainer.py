import os,sys
import numpy as np
from Network_Security.entity.config_entity import ModelTrainerConfig
from Network_Security.entity.artifact_entity import DataTransformationArtifact,ModelTrainerArtifact,ClassificationMetricArtifact
from Network_Security.logging.logger import logging
from Network_Security.exception.exception import NetworkSecurityException

from Network_Security.utils.main_utils.utils import save_object,save_numpy_arr_data,load_object,load_numpy_arr_data
from Network_Security.utils.ml_utils.metric.classification_metric import get_classification_score
from Network_Security.utils.ml_utils.model.estimator import NetworkModel

class ModelTrainer:
    def __init__(self,model_trainer_config:ModelTrainerConfig,data_transformation_artifact:DataTransformationArtifact):
        try:
            self.model_trainer_config=model_trainer_config
            self.data_transformation_artifact=data_transformation_artifact
        except Exception as e:
            raise NetworkSecurityException(e,sys)

    def train_model(self,x_train,y_train):
        pass
    
    def initiate_model_trainer(self)->ModelTrainerArtifact :
        try:
            train_file_path=self.data_transformation_artifact.transformed_train_file_path
            test_file_path=self.data_transformation_artifact.transformed_test_file_path
            train_arr=load_numpy_arr_data(train_file_path)
            test_arr=load_numpy_arr_data(test_file_path)
            x_train,x_test,y_train,y_test=(
                train_arr[:,:-1],
                test_arr[:,:-1],
                train_arr[:,-1],
                test_arr[:,-1]
            )
            model=self.train_model(x_train,y_train)
        except Exception as e:
            raise NetworkSecurityException(e,sys)