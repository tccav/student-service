from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.resources import Resource, SERVICE_NAME
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from sanic import Sanic, Request
from sanic.response import json, text
from sanic_ext import Extend, openapi
from sanic import exceptions
from mayim.exception import RecordNotFound
from mayim.extension import SanicMayimExtension
import json_logging
from sanic_ext.extensions.openapi.definitions import Response

from app import telemetry
from models import Student
from executors import StudentExecutor
from validations import StudentValidator
from psycopg.errors import UniqueViolation
import os

resource = Resource(attributes={
    SERVICE_NAME: "student-service"
})
tracer_provider = TracerProvider(resource=resource)
tracer_processor = BatchSpanProcessor(OTLPSpanExporter(endpoint="localhost:4317", insecure=True))
tracer_provider.add_span_processor(tracer_processor)
trace.set_tracer_provider(tracer_provider)

app = Sanic("StudentServiceApp")
json_logging.init_sanic(enable_json=True)
json_logging.init_request_instrument(app)

app.ctx.db = f"postgres://{os.environ['DB_USER']}:{os.environ['DB_PASSWORD']}@{os.environ['DB_HOST']}:" \
             f"{os.environ['DB_PORT']}/{os.environ['DB_NAME']}?{os.environ['DB_OPTIONS']}"

Extend.register(
    SanicMayimExtension(
        executors=[StudentExecutor],
        dsn=app.ctx.db
    )
)


@app.get("/healthcheck")
async def healthcheck(_):
    return text("RUNNING")


@app.get("/students/<student_id>")
@telemetry.start_as_current_http_span()
@openapi.response(response=Response(content={"application/json": Student}, status=200))
async def get_student(_: Request, student_id: str, executor: StudentExecutor):
    try:
        student = await executor.get_user(student_id)
        return json(student.__dict__, ensure_ascii=False, default=str)
    except RecordNotFound:
        raise exceptions.NotFound(f"Could not find student with id = {student_id}")


@app.post("/students/")
@telemetry.start_as_current_http_span()
@openapi.body(Student)
@openapi.response(status=201, content=Student)
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

        return json(body=student.__dict__, status=201, ensure_ascii=False, default=str)

    except ValueError as e:
        raise exceptions.BadRequest(f"{e}")

    except UniqueViolation as e:
        raise exceptions.BadRequest(f"Already exists student with this id.")

    except Exception as e:
        raise exceptions.ServerError(f"Unexpected error: {e}")


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8001, access_log=True)
