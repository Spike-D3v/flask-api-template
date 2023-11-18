from logging.config import dictConfig

from flask import Flask, jsonify


def create_app(settings_module: str) -> Flask:
    """Devuelve una instancia de la aplicación"""
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(settings_module)

    # Configuración Local
    config_file = "config.py"
    if app.config.get("TESTING", False):
        config_file = "config_testing.py"
    app.config.from_pyfile(config_file, silent=True)

    # Configurar logging
    __configure_logging(app)

    # Inicializar Extensiones
    __load_extensions(app)

    # Registrar Error Handlers
    __register_error_handlers(app)

    # Registrar Blueprints
    __register_blueprints(app)

    return app


def __configure_logging(app: Flask) -> None:
    """Configurar logging"""

    if "LOGGING" not in app.config:
        return

    for handler in app.logger.handlers:
        app.logger.removeHandler(handler)

    dictConfig(app.config["LOGGING"])


def __load_extensions(app: Flask) -> None:
    """Importar y e inicializar las extensiones de la app"""
    from .db import db
    from .extensions import migrations, ma, jwt, cors

    db.init_app(app)
    migrations.init_app(app, db)
    ma.init_app(app)
    cors.init_app(app)
    jwt.init_app(app)


def __register_blueprints(app: Flask) -> None:
    """Importar y registrar blueprints"""
    from app.auth import auth
    from app.public import public

    app.register_blueprint(public)
    app.register_blueprint(auth)


def __register_error_handlers(app: Flask) -> None:
    """Registrar error handlers del sistema"""
    from app.core import exceptions as exc

    @app.errorhandler(Exception)
    @app.errorhandler(500)
    def general_error_handler(e):
        app.logger.debug(e, exc_info=True)
        app.logger.error("Unexpected server error")
        return jsonify(message="Internal Server Error"), 500

    @app.errorhandler(NotImplementedError)
    def not_implemented_error_handler(e):
        app.logger.debug(e, exc_info=True)
        app.logger.warning("Incomplete feature requested")
        return jsonify(message="Sorry! Feature under construction"), 500

    @app.errorhandler(405)
    def not_allowed_handler(e):
        return jsonify(message="Method not allowed"), 405

    @app.errorhandler(404)
    def general_not_found_error_handler(e):
        return jsonify(message="Resource not found"), 404

    @app.errorhandler(exc.NotFoundError)
    def not_found_error_handler(e: exc.BaseApiError):
        return jsonify(e.to_dict()), e.status_code

    @app.errorhandler(exc.PermissionsError)
    def permissions_error_handler(e: exc.BaseApiError):
        return jsonify(e.to_dict()), e.status_code

    @app.errorhandler(exc.NotAuthorizedError)
    def not_authorized_error_handler(e: exc.BaseApiError):
        return jsonify(e.to_dict()), e.status_code

    @app.errorhandler(exc.BadRequestError)
    def bad_request_error_handler(e: exc.BaseApiError):
        return jsonify(e.to_dict()), e.status_code
