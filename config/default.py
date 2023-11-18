from os.path import abspath, dirname, join

BASE_DIR = dirname(dirname(abspath(__file__)))
MEDIA_ROOT = join(BASE_DIR, "media")
LOGS_ROOT = join(BASE_DIR, "logs")

SECRET_KEY = "supersecret"
TESTING = False
DEBUG = True

# SQLAlchemy
SQLALCHEMY_TRACK_MODIFICATIONS = False

# JWT
JWT_SECRET_KEY = "ultra-secret"
JWT_TOKEN_LOCATION = ["cookies"]
JWT_COOKIE_SECURE = False

# Environments
APP_ENV_DEVELOPMENT = "development"
APP_ENV_TESTING = "testing"
APP_ENV_STAGING = "staging"
APP_ENV_PRODUCTION = "production"
APP_ENV_LOCAL = "local"
APP_ENV = ""

LOGGING = {
    "version": 1,
    "disable_existing_loggers": True,
    "formatters": {
        "default": {
            "format": "[%(name)s] [%(asctime)s.%(msecs)d] (%(levelname)s): %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
        "request": {
            "class": "app.logger.RequestFormatter",
            "format": "[%(name)s] [%(asctime)s.%(msecs)d] [%(endpoint)s - %(method)s] (%(levelname)s): %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
    },
    "handlers": {
        "default": {
            "level": "DEBUG" if DEBUG else "INFO",
            "class": "logging.StreamHandler",
            "formatter": "default",
        },
        "console": {
            "level": "DEBUG" if DEBUG else "INFO",
            "class": "logging.StreamHandler",
            "formatter": "request",
        },
        "root_file": {
            "level": "DEBUG" if DEBUG else "INFO",
            "class": "logging.FileHandler",
            "filename": join(LOGS_ROOT, "app.log"),
            "formatter": "request",
        },
    },
    "loggers": {
        "app": {
            "handlers": ["console", "root_file"],
            "level": "DEBUG" if DEBUG else "INFO",
            "propagate": False,
        }
    },
    "root": {
        "handlers": ["default"],
        "level": "DEBUG" if DEBUG else "INFO",
    },
}
