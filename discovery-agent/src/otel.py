from __future__ import annotations
from opentelemetry import trace
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.httpx import HTTPXClientInstrumentor

_initialized = False

def setup_tracing(service_name: str, endpoint: str | None):
    global _initialized
    if _initialized:
        return
    provider = TracerProvider(resource=Resource.create({"service.name": service_name}))
    if endpoint:
        exporter = OTLPSpanExporter(endpoint=endpoint)
        provider.add_span_processor(BatchSpanProcessor(exporter))
    trace.set_tracer_provider(provider)
    HTTPXClientInstrumentor().instrument()
    _initialized = True

def get_tracer(name: str):
    return trace.get_tracer(name)
