from mayim import PostgresExecutor, query
from models import Student

class StudentExecutor(PostgresExecutor):

    @query("SELECT * FROM students WHERE id = $id")
    async def get_user(self, id) -> Student:
        ...
    
    @query("INSERT INTO students (id, name, cpf, birth_date, email, course_id) VALUES ($id, $name, $cpf, $birth_date, $email, $course_id)")
    async def register_user(self, id, name, cpf, birth_date, email, course_id):
        ...


