from dataclasses import dataclass
from datetime import date
import uuid


@dataclass
class Student:
    id: int
    name: str
    cpf: str
    birth_date: date
    email: str
    course_id: uuid.UUID






