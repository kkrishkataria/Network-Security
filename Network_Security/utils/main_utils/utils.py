import os,sys
import yaml
import pickle
from Network_Security.logging.logger import logging
from Network_Security.exception.exception import NetworkSecurityException

def read_yaml_file(filepath:str)->dict:
    try:
        with open(filepath) as yaml_file:
            return yaml.safe_load(yaml_file)
    except Exception as e:
        raise NetworkSecurityException(e,sys)