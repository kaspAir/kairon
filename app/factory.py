from flask import Flask

from app.config import get_config
from app.domains.decision.routes import bp as decision_bp
from app.domains.governance.routes import bp as governance_bp
from app.domains.scenario.routes import bp as scenario_bp
from app.domains.simulation.routes import bp as simulation_bp
from app.shared.database import SessionLocal, init_engine
from app.shared.errors import register_error_handlers
from app.shared.logging import configure_logging, register_request_logging
from app.web.routes import api as core_bp


def create_app(config_class=None):
    app = Flask(__name__)
    app.config.from_object(config_class or get_config())

    configure_logging(app)
    register_error_handlers(app)
    register_request_logging(app)

    init_engine(app.config["DATABASE_URL"], echo=app.config.get("SQL_ECHO", False))

    _register_blueprints(app, url_prefix="/api")
    _register_blueprints(app, name_prefix="legacy")

    @app.teardown_appcontext
    def remove_session(exception=None):
        SessionLocal.remove()

    return app


def _register_blueprints(app, url_prefix=None, name_prefix=None):
    registrations = [core_bp, decision_bp, scenario_bp, simulation_bp, governance_bp]
    for blueprint in registrations:
        kwargs = {}
        if url_prefix:
            kwargs["url_prefix"] = url_prefix
        if name_prefix:
            kwargs["name"] = f"{name_prefix}_{blueprint.name}"
        app.register_blueprint(blueprint, **kwargs)
