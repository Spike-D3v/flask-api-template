from .default import *

APP_ENV = APP_ENV_LOCAL
LOGGING["loggers"]["app"]["handlers"] = ["console"]
