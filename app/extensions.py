from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate

migrations = Migrate()
ma = Marshmallow()
cors = CORS()
jwt = JWTManager()
