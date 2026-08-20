import sys,os
import numpy as np 
import pandas as pd
from sklearn.impute import KNNImputer
from sklearn.pipeline import Pipeline
from Network_Security.logging.logger import logging
from Network_Security.exception.exception import NetworkSecurityException
from Network_Security.constants.training_pipeline import TARGET_COLUMN
from Network_Security.constants.training_pipeline import DATA_TRANSFORMATION_IMPUTER_PARAMS
from Network_Security.entity.artifact_entity import DataTransformationArtifact,DataValidationArtifact
from Network_Security.entity.config_entity import DataTransformationConfig
from Network_Security.utils.main_utils.utils import save_numpy_arr_data,save_object

class DataTransformation:
    def __init__(self,data_transformation_config:DataTransformationConfig,data_validation_artifact:DataValidationArtifact):
        try:
            self.data_validation_artifact=data_validation_artifact
            self.data_transformation_config=data_transformation_config
        except Exception as e:
            raise NetworkSecurityException(e,sys)

    @staticmethod
    def read_data(filepath)->pd.DataFrame:
        try:
            with open(filepath,'r') as file:
                return pd.read_csv(file)
        except Exception as e:
                    raise NetworkSecurityException(e,sys)

    def get_data_transformer_obj(self,)->Pipeline:
         logging.info("Entered get_data_transformer_obj function")
         try:
              knn=KNNImputer(**DATA_TRANSFORMATION_IMPUTER_PARAMS)
              processor:Pipeline=Pipeline([
                   ("knn",knn),
              ]
              )
              return processor
         except Exception as e:
                     raise NetworkSecurityException(e,sys)
         
    def initiate_data_transformation(self)->DataTransformationArtifact:
        try:
            logging.info("Initiating Data Transformation")
            train_df=DataTransformation.read_data(self.data_validation_artifact.valid_train_file_path)
            test_df=DataTransformation.read_data(self.data_validation_artifact.valid_test_file_path)
            input_train_df=train_df.drop([TARGET_COLUMN],axis=1)
            target_train_df=train_df[TARGET_COLUMN]
            input_test_df=test_df.drop([TARGET_COLUMN],axis=1)
            target_test_df=test_df[TARGET_COLUMN]
            target_train_df.replace(-1,0,inplace=True)
            target_test_df.replace(-1,0,inplace=True)
            preprocessor=self.get_data_transformer_obj()
            preprocessor_model=preprocessor.fit(input_train_df)
            input_train_tranform_data=preprocessor.transform(input_train_df)
            input_test_tranform_data=preprocessor.transform(input_test_df)
            train_arr=np.c_[input_train_tranform_data,np.array(target_train_df)]
            test_arr=np.c_[input_test_tranform_data,np.array(target_test_df)]
            save_object("final_model/preprocessor.pkl",preprocessor) 
            save_numpy_arr_data(self.data_transformation_config.transformed_train_file_path,train_arr)
            save_numpy_arr_data(self.data_transformation_config.transformed_test_file_path,test_arr)

            save_object(self.data_transformation_config.transformed_object_file_path,preprocessor_model)
            data_transformation_artifact=DataTransformationArtifact(self.data_transformation_config.transformed_object_file_path,self.data_transformation_config.transformed_train_file_path,self.data_transformation_config.transformed_test_file_path)
            return data_transformation_artifact
        except Exception as e:
            raise NetworkSecurityException(e,sys)

