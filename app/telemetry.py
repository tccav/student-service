import functools
from typing import Dict

from opentelemetry import trace
from opentelemetry.semconv.trace import SpanAttributes
from opentelemetry.trace import SpanKind
from opentelemetry.trace.propagation.tracecontext import TraceContextTextMapPropagator
from sanic import Request

HTTP_DEFAULT_ATTRIBUTES = {
    SpanAttributes.HTTP_SCHEME: "http",
    SpanAttributes.HTTP_FLAVOR: "1.1",
}


def start_as_current_http_span():
    def decorator_start_as_current_http_span(func):
        @functools.wraps(func)
        async def wrapper_start_as_current_http_span(*args, **kwargs):
            req: Request = args[0]
            attributes = {}
            ctx = None
            if req is not None:
                attributes.setdefault(SpanAttributes.HTTP_URL, req.url)
                attributes.setdefault(SpanAttributes.HTTP_METHOD, req.method)
                attributes.setdefault(SpanAttributes.HTTP_ROUTE, req.route.path)
                attributes.setdefault(SpanAttributes.HTTP_USER_AGENT, req.headers.get("user-agent"))

                if req.headers.get("traceparent"):
                    try:
                        carrier = _traceparent_header_to_carrier(req.headers.get("traceparent"))
                        ctx = TraceContextTextMapPropagator().extract(carrier)
                    except AttributeError:
                        pass

            with tp.start_as_current_span(f"{req.method} /{req.route.path}",
                                          context=ctx,
                                          kind=SpanKind.SERVER,
                                          attributes={
                                              SpanAttributes.HTTP_SCHEME: "http",
                                              SpanAttributes.HTTP_FLAVOR: "1.1",
                                              **attributes
                                          }) as span:
                func_return = await func(*args, **kwargs)

                span.set_attribute(SpanAttributes.HTTP_STATUS_CODE, func_return.status)

            return func_return

        return wrapper_start_as_current_http_span

    tp = trace.get_tracer("app.http.server")

    return decorator_start_as_current_http_span


def _traceparent_header_to_carrier(traceparent: str) -> dict:
    return {"traceparent": traceparent}
