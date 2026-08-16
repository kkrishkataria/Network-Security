import os,sys
import yaml
import pickle
from Network_Security.logging.logger import logging
from Network_Security.exception.exception import NetworkSecurityException

def read_yaml_file(filepath:str)->dict:
    try:
        with open(filepath,'rb') as yaml_file:
            return yaml.safe_load(yaml_file)
    except Exception as e:
        raise NetworkSecurityException(e,sys)
    
def write_yaml_file(filepath:str,content:object,replace:bool=False)->dict:
    try:
        if replace:
            if(os.path.exists(filepath)):
                os.remove(filepath)
        os.makedirs(os.path.dirname(filepath),exist_ok=True)
        with open(filepath,"w") as file:
            return yaml.dump(content,file)
    except Exception as e: 
        raise NetworkSecurityException(e,sys)