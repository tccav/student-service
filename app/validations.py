from executors import StudentExecutor
import re
from datetime import datetime

class StudentValidator:
    def __init__(self) -> None:
        self.student_executor = StudentExecutor

    def __validate_id(self, request: dict) -> None:
        if not "id" in request:
            raise ValueError("Id field is required.")
        value = request["id"]
        if not isinstance(value, int):
            raise ValueError("Id needs be int type.")
    
    def __validate_name(self, request: dict) -> None:
        if not "name" in request:
            raise ValueError("Name field is required.")
    
    def __validate_cpf(self, request: dict) -> None:
        if not "cpf" in request:
            raise ValueError("cpf field is required.")

    def __validate_email(self, request: dict) -> None:
        if not "email" in request:
            raise ValueError("Email field is required.")
        value = request["email"]
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
        if not re.fullmatch(regex, value):
            raise ValueError("Email is not valid.")
    
    def __validate_birth_date(self, request: dict) -> None:
        if not "birth_date" in request:
            raise ValueError("birth_date field is required.")
        value = request["birth_date"]
        try:
            datetime.strptime(value, "%Y-%m-%d")
        except:
            raise ValueError("birth_date field bad format. The expected date format is YYYY-MM-DD.")
    
    def __validate_course_id(self, request: dict) -> None:
        if not "course_id" in request:
            raise ValueError("course_id field is required.")    
    
    def is_request_valid(self, request: dict) -> bool:
        self.__validate_cpf(request)
        self.__validate_email(request)
        self.__validate_id(request)
        self.__validate_name(request)
        self.__validate_birth_date(request)
        self.__validate_course_id(request)
        
    
        