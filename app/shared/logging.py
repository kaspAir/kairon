import logging
import sys
import time
from uuid import uuid4

from flask import g, has_request_context, request


class RequestContextFilter(logging.Filter):
    def filter(self, record):
        if has_request_context():
            record.request_id = getattr(g, "request_id", "-")
            record.method = request.method
            record.path = request.path
        else:
            record.request_id = "-"
            record.method = "-"
            record.path = "-"
        return True


def configure_logging(app):
    level = getattr(logging, app.config.get("LOG_LEVEL", "INFO").upper(), logging.INFO)
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s request_id=%(request_id)s method=%(method)s path=%(path)s logger=%(name)s message="%(message)s"'
    ))
    handler.addFilter(RequestContextFilter())

    root = logging.getLogger()
    root.handlers.clear()
    root.setLevel(level)
    root.addHandler(handler)

    app.logger.setLevel(level)


def register_request_logging(app):
    @app.before_request
    def before_request():
        g.request_id = request.headers.get("X-Request-ID", str(uuid4()))
        g.request_started_at = time.perf_counter()

    @app.after_request
    def after_request(response):
        duration_ms = round((time.perf_counter() - g.get("request_started_at", time.perf_counter())) * 1000, 2)
        app.logger.info("request_completed status=%s duration_ms=%s", response.status_code, duration_ms)
        response.headers["X-Request-ID"] = g.request_id
        return response
