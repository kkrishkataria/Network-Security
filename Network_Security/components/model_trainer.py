import os,sys
import numpy as np
import mlflow
from Network_Security.entity.config_entity import ModelTrainerConfig
from Network_Security.entity.artifact_entity import DataTransformationArtifact,ModelTrainerArtifact,ClassificationMetricArtifact
from Network_Security.logging.logger import logging
from Network_Security.exception.exception import NetworkSecurityException

from Network_Security.utils.main_utils.utils import save_object,save_numpy_arr_data,load_object,load_numpy_arr_data,evaluate_model
from Network_Security.utils.ml_utils.metric.classification_metric import get_classification_score
from Network_Security.utils.ml_utils.model.estimator import NetworkModel

from sklearn.linear_model import LogisticRegression
from sklearn.metrics import r2_score
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import (
    AdaBoostClassifier,
    GradientBoostingClassifier,
    RandomForestClassifier
)

class ModelTrainer:
    def __init__(self,model_trainer_config:ModelTrainerConfig,data_transformation_artifact:DataTransformationArtifact):
        try:
            self.model_trainer_config=model_trainer_config
            self.data_transformation_artifact=data_transformation_artifact
        except Exception as e:
            raise NetworkSecurityException(e,sys)

    def track_mlflow(self,best_model,classification_metric:ClassificationMetricArtifact):
        with mlflow.start_run():
            f1_score=classification_metric.f1_score
            precision_score=classification_metric.precision_score
            recall_score=classification_metric.recall_score
            mlflow.log_metric("f1 score",f1_score)
            mlflow.log_metric("precision_score",precision_score)
            mlflow.log_metric("recall_score",recall_score)
            mlflow.sklearn.log_model(best_model,"Model")

    

    def train_model(self,x_train,y_train,x_test,y_test):

        models = {
        "Random Forest": RandomForestClassifier(verbose=1),
        "Decision Tree": DecisionTreeClassifier(),
        "Gradient Boosting": GradientBoostingClassifier(verbose=1),
        "Logistic Regression": LogisticRegression(verbose=1),
        "AdaBoost": AdaBoostClassifier(),
    }

        params = {
                "Decision Tree": {
                    "criterion": ["gini", "entropy"],
                },
            
                "Random Forest": {
                    "n_estimators": [32, 64],
                },
            
                "Gradient Boosting": {
                    "learning_rate": [0.1, 0.01],
                    "subsample": [0.8],
                    "n_estimators": [32, 64],
                },
            
                "Logistic Regression": {},
            
                "AdaBoost": {
                    "learning_rate": [0.1, 0.5],
                    "n_estimators": [32, 64],
                }
            }

        model_report:dict=evaluate_model(x_train,y_train,x_test,y_test,models,params)

        best_model_score=max(sorted(model_report.values()))
        best_model_name=list(model_report.keys())[list(model_report.values()).index(best_model_score)]
        best_model=models[best_model_name]
        y_pred_train=best_model.predict(x_train)
        y_pred_test=best_model.predict(x_test)
        classification_train_metric:ClassificationMetricArtifact=get_classification_score(y_train,y_pred_train)
        classification_test_metric:ClassificationMetricArtifact=get_classification_score(y_test,y_pred_test)

        self.track_mlflow(best_model,classification_train_metric)
        self.track_mlflow(best_model,classification_test_metric)
        preprocessor=load_object(self.data_transformation_artifact.transformed_object_file_path)
        dir_path=os.path.dirname(self.model_trainer_config.trained_model_file_path)
        os.makedirs(dir_path,exist_ok=True)
        network_model=NetworkModel(preprocessor,best_model)
        save_object(self.model_trainer_config.trained_model_file_path,network_model)
        model_trainer_artifact=ModelTrainerArtifact(self.model_trainer_config.trained_model_file_path,classification_train_metric,classification_test_metric)
        return model_trainer_artifact

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
            model_trainer_artifact=self.train_model(x_train,y_train,x_test,y_test)
            return model_trainer_artifact
        except Exception as e:
            raise NetworkSecurityException(e,sys)