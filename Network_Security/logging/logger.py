import logging
import os 
from datetime import datetime

LOG_FILE=f"{datetime.now().strftime('%m_%d_%y_%H_%M_%S')}.log"
logs_path=os.path.join(os.getcwd(),"logs")
logs_path_file=os.path.join(os.getcwd(),"logs",LOG_FILE)
os.makedirs(logs_path,exist_ok=True)

logging.basicConfig(
    filename=logs_path_file,
    format='[%(asctime)s] %(name)s - %(levelname)s - Line %(lineno)d - %(message)s',
    level=logging.INFO
)
