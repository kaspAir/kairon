from marshmallow import ValidationError
from sqlalchemy.exc import SQLAlchemyError
from werkzeug.exceptions import HTTPException


class NotFoundError(ValueError):
    pass


def error_payload(message, status_code, code=None, details=None):
    payload = {
        "error": {
            "code": code or "error",
            "message": message,
            "status": status_code,
        }
    }
    if details:
        payload["error"]["details"] = details
    return payload


def register_error_handlers(app):
    @app.errorhandler(ValidationError)
    def handle_validation_error(exc):
        return error_payload("Request validation failed", 400, "validation_error", exc.messages), 400

    @app.errorhandler(NotFoundError)
    def handle_not_found(exc):
        return error_payload(str(exc), 404, "not_found"), 404

    @app.errorhandler(ValueError)
    def handle_value_error(exc):
        return error_payload(str(exc), 400, "bad_request"), 400

    @app.errorhandler(SQLAlchemyError)
    def handle_database_error(exc):
        app.logger.exception("database_error")
        return error_payload("Database operation failed", 500, "database_error"), 500

    @app.errorhandler(HTTPException)
    def handle_http_exception(exc):
        return error_payload(exc.description, exc.code, exc.name.lower().replace(" ", "_")), exc.code

    @app.errorhandler(Exception)
    def handle_unexpected_error(exc):
        app.logger.exception("unhandled_exception")
        return error_payload("Internal server error", 500, "internal_server_error"), 500
