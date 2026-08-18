import os,sys
import yaml
import pickle
import numpy as np
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

def save_numpy_arr_data(filepath:str,arr:np.array): # location of npy file 
    try:
        dir_path=os.path.dirname(filepath)
        os.makedirs(dir_path,exist_ok=True)
        with open(filepath,'wb') as file:
            np.save(file,arr) # to store in npy file 
    except Exception as e:
        raise NetworkSecurityException(e,sys)
    
def load_numpy_arr_data(filepath:str): 
    try:
        if not os.path.exists(filepath):
            raise Exception(f"The file {filepath} not Exists")
        with open(filepath,'wb') as file:
            return np.load(file) 
    except Exception as e:
        raise NetworkSecurityException(e,sys)

def save_object(filepath:str,obj:object):
    try:
        dir_path=os.path.dirname(filepath)
        os.makedirs(dir_path,exist_ok=True)
        with open(filepath,'wb') as file:
            pickle.dump(obj,file)
    except Exception as e:
        raise NetworkSecurityException(e,sys)
 
def load_object(filepath:str):
    try:
        if not os.path.exists(filepath):
            raise Exception(f"The file {filepath} not Exists")
        with open(filepath,'rb') as file:
            return pickle.load(file)
    except Exception as e:
        raise NetworkSecurityException(e,sys)

