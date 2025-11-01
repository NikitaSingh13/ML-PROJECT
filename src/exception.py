# You can go and search 'exception python' and you'll get already written code for exception handling
# But here the code written is custom exception handling (hand-written logic for better traceability)

import sys   # sys module provides access to variables used or maintained by the Python interpreter
from src.logger import logging


def error_message_detail(error, error_detail: sys):
    """
    This function extracts detailed error information like
    file name, line number, and actual error message.
    """
    _, _, exc_tb = error_detail.exc_info()
    file_name = exc_tb.tb_frame.f_code.co_filename
    error_message = "Error occurred in python script name [{0}] line number [{1}] error message [{2}]".format(
        file_name, exc_tb.tb_lineno, str(error)
    )
    return error_message


class CustomException(Exception):
    """
    Custom Exception class that captures detailed error information
    using the error_message_detail() helper function.
    """
    def __init__(self, error_message, error_detail: sys):
        super().__init__(error_message)
        self.error_message = error_message_detail(
            error_message, error_detail=error_detail
        )

    def __str__(self):
        return self.error_message
