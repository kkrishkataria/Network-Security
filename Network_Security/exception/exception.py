import sys
from Network_Security.logging.logger import logging

def error_message_detail(error,error_detail:sys):
    _,_,exc_tb=error_detail.exc_info() # first 2 info not needed exc_tb that is exception 
    # traceback is required for exception features like line no and file name where occured

    file_name=exc_tb.tb_frame.f_code.co_filename
    err_msg="Error occured in Python Script name [{0}] line number [{1}] Error Message [{2}]".format(
        file_name,exc_tb.tb_lineno,str(error)
    )
    return err_msg
class NetworkSecurityException(Exception):
    def __init__(self, error_message,error_detail:sys):
        super().__init__(error_message)
        self.error_message=error_message_detail(error_message,error_detail)

    def __str__(self):
        return self.error_message

# if __name__=="__main__":
#     try:
#         a=1/0
#     except Exception as e:
#         logging.info("Divide by zero")
#         raise NetworkSecurityException(e,sys)
