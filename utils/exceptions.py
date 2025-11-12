import sys

def get_error_message_details(error, error_detail: sys):
    """
    This function will return the error message details
    
    param error: Exception : The exception object
    param error_detail: sys : The sys module to get the traceback details
    return: str : The error message details
    """
    _, _, exc_tb = error_detail.exc_info()
    file_name = exc_tb.tb_frame.f_code.co_filename
    line_number = exc_tb.tb_lineno
    error_message = f"Error occurred in script: {file_name} at line number: {line_number} with message: {str(error)}"
    return error_message

class APIError(Exception):
    """
    custom exception for API errors
    
    Attributes:
        message (str): Description of the error.
        status_code (int): HTTP status code associated with the error.
    """
    def __init__(self, message: str, status_code: int = None):
        self.message = get_error_message_details(message, sys)
        self.status_code = status_code
        super().__init__(self.message)

    def __str__(self):
        if self.status_code:
            return f"APIError {self.status_code}: {self.message}"
        return f"APIError: {self.message}"
    
class configError(Exception):
    """
    custom exception for configuration errors
    
    Attributes:
        message (str): Description of the error.
    """
    def __init__(self, message: str):
        self.message = get_error_message_details(message, sys)
        super().__init__(self.message)

    def __str__(self):
        return f"ConfigError: {self.message}"

    ## will define more as per the requirements