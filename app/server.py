from sanic import Sanic, Request
from sanic.response import json, text
from sanic_ext import Extend, openapi
from sanic import exceptions
from mayim.exception import RecordNotFound
from mayim.extension import SanicMayimExtension
from models import Student
from executors import StudentExecutor
from validations import StudentValidator
from psycopg.errors import UniqueViolation
import os


app = Sanic("StudentServiceApp")
app.ctx.db = f"postgres://{os.environ['DB_USER']}:{os.environ['DB_PASSWORD']}@{os.environ['DB_HOST']}:{os.environ['DB_PORT']}/{os.environ['DB_NAME']}?{os.environ['DB_OPTIONS']}"

Extend.register(
    SanicMayimExtension(
        executors=[StudentExecutor],
        dsn=app.ctx.db
    )
)

@app.get("/healthcheck")
async def healthcheck(request):
    return text("RUNNING")


@app.get("/student/<id>")
@openapi.response(Student)
async def get_student(request: Request, id:str, executor: StudentExecutor):
    try:
        student = await executor.get_user(id)
        return json(student.__dict__ , ensure_ascii=False, default=str)
    except RecordNotFound:
        raise exceptions.NotFound(f"Could not find student with id = {id}")


@app.post("/student/")
@openapi.body(Student)
async def post_student(request: Request, executor: StudentExecutor):

    body = request.json
    validator = StudentValidator()

    try:
        validator.is_request_valid(body)

        student = Student(
            body.get("id"),
            body.get("name"),
            body.get("cpf"),
            body.get("birth_date"),
            body.get("email"),
            body.get("course_id")
        )

        await executor.register_user(
            student.id, 
            student.name, 
            student.cpf, 
            student.birth_date, 
            student.email,
            student.course_id)
                
        return json(student.__dict__ , ensure_ascii=False, default=str)
        
    except ValueError as e:
        raise exceptions.BadRequest(f"{e}")
    
    except UniqueViolation as e:
        raise exceptions.BadRequest(f"Already exists student with this id.")


if __name__ == '__main__':
    app.run(host="app", port=8000)
