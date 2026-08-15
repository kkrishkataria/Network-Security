import os,sys,json,certifi
from dotenv import load_dotenv
import pandas as pd 
import numpy as np 
import pymongo 
from Network_Security.logging.logger import logging
from Network_Security.exception.exception import NetworkSecurityException


load_dotenv()
MONGO_DB_URL=os.getenv("MONGO_DB_URL")
# print(MONGO_DB_URL)

ca=certifi.where()

class Network_Data_Extract:
    def __init__(self):
        try:
            pass
        except Exception as e:
            raise NetworkSecurityException(e,sys)

    def csv_to_json_convertor(self,filepath):
        try:
            data=pd.read_csv(filepath)
            data.reset_index(drop=True,inplace=True)
            records=list(json.loads(data.T.to_json()).values())
            return records
        
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def insert_data_to_mongo(self,records,database,collection):
        try:
            self.database=database
            self.collection=collection
            self.records=records
            self.mongo_client=pymongo.MongoClient(MONGO_DB_URL)

            self.database=self.mongo_client[self.database]
            self.collection=self.database[self.collection]
            self.collection.insert_many(self.records)
            return len(self.records)
                
        except Exception as e:
            raise NetworkSecurityException(e,sys)

if __name__=='__main__':
    FILE_PATH="Network_Data/phisingData.csv"
    DATABASE="KRISH"
    COLLECTION="NetworkData"
    obj=Network_Data_Extract()
    records=obj.csv_to_json_convertor(FILE_PATH)
    number_of_rec=obj.insert_data_to_mongo(records,DATABASE,COLLECTION)
    print(number_of_rec)