import sys,os
from Network_Security.entity.artifact_entity import DataIngestionArtifact,DataValidationArtifact
from Network_Security.entity.config_entity import DataValidationConfig
from Network_Security.logging.logger import logging
from Network_Security.exception.exception import NetworkSecurityException
from Network_Security.utils.main_utils.utils import read_yaml_file,write_yaml_file
from Network_Security.constants.training_pipeline import SCHEMA_FILE_PATH

from scipy.stats import ks_2samp # to check data drift bw two samples 
import pandas as pd 

class DataValidaton:
    def __init__(self,data_ingestion_artifact:DataIngestionArtifact,data_validation_config:DataValidationConfig):
        try:
            self.data_ingestion_artifact=data_ingestion_artifact
            self.data_validation_config=data_validation_config
            self._schema_config=read_yaml_file(SCHEMA_FILE_PATH)

        except Exception as e:
            raise NetworkSecurityException(e,sys)

    @staticmethod # can call directly through class no self req and no obj req to call
    def read_data(filepath)->pd.DataFrame:
        try:
            df=pd.read_csv(filepath)
            return df
        except Exception as e:
            raise NetworkSecurityException(e,sys)

    def validate_number_of_columns(self,df:pd.DataFrame)->bool:
        try:
            no_of_colums=len(self._schema_config)
            logging.info(f"Required Number of Columns: {no_of_colums}")
            logging.info(f"DataFrame has Number of Columns as : {len(df.columns)}")
            if(len(df.columns)==no_of_colums):
                return True
            return False
            
        except Exception as e:
            NetworkSecurityException(e,sys)

    def detect_data_drift(self,base_df:pd.DataFrame,curr_df:pd.DataFrame,threshold=0.05)->bool:
        try:
            status=True
            report={}
            for column in base_df.columns:
                d1=base_df[column]
                d2=curr_df[column]
                is_sam_dist=ks_2samp(d1,d2)
                if threshold<=is_sam_dist.pvalue:
                    isFound=False
                else:
                    isFound=True
                    status=False
                report.update({column:{
                    "pvalue":float(is_sam_dist.pvalue),
                    "drift_status":isFound
                }})
            drift_report_file_path=self.data_validation_config.drift_report_file_path
            write_yaml_file(drift_report_file_path,report)
            return status
        except Exception as e:
            raise NetworkSecurityException(e,sys)

    def initiate_data_validation(self)->DataValidationArtifact:
        try:
            train_file_path=self.data_ingestion_artifact.train_file_path
            test_file_path=self.data_ingestion_artifact.test_file_path

            train_df=DataValidaton.read_data(train_file_path)
            test_df=DataValidaton.read_data(test_file_path)

            status=self.validate_number_of_columns(train_df)
            if not status:
                error_msg=f"Train DataFrame dont have all Columns.\n"

            status=self.validate_number_of_columns(test_df)
            if not status:
                error_msg=f"Test  DataFrame dont have all Columns.\n"

            status=self.detect_data_drift(train_df,test_df)
            dir_path=os.path.dirname(self.data_validation_config.valid_train_file_path)
            os.makedirs(dir_path,exist_ok=True)
            train_df.to_csv(self.data_validation_config.valid_train_file_path,index=False,header=True)
            test_df.to_csv(self.data_validation_config.valid_test_file_path,index=False,header=True)

            data_validation_artifact= DataValidationArtifact(
                    validation_status= status,
                    valid_train_file_path=train_file_path,
                    valid_test_file_path= test_file_path,
                    invalid_train_file_path= None,
                    invalid_test_file_path= None,
                    drift_report_file_path= self.data_validation_config.drift_report_file_path)
            return data_validation_artifact
        
        except Exception as e:
            raise NetworkSecurityException(e,sys)
