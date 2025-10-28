#  you can go and search 'exception python' and you'll get already written code for exception handline
# but here the code written is custom exception handling means hand written code all

import sys   #sys module proides various functions & variables that're used to manipulate diff parts of the python runtime environment

def error_message_detail(error, error_detail: sys):
    _,_,exc_tb = error_detail.exc_info()
    fine_name = exc_tb.tb_frame.f_code.co_filename
    error_message = "Error occured in python script name [{0}] line number[{1}] error message[{2}]".format(
    fine_name, exc_tb.tb_lineno, str(error))

    return error_message

    

class CustomException(Exception):
    def __init__(self, error_message, error_detail:sys):
        super().__init__(error_message)
        self.error_message = error_message_detail(error_message, error_detail=error_detail)

    def __str__(self):
        return self.error_message
