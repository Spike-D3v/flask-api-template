from flask import request, jsonify
from flask_jwt_extended import (
    create_access_token,
    set_access_cookies,
    current_user,
    unset_access_cookies,
    jwt_required,
)

from app.core.exceptions import NotAuthorizedError
from . import auth
from .decorators import role_required
from .models import User
from .schemas import LoginSchema, UserSchema

user_schema = UserSchema()
login_schema = LoginSchema()
signup_schema = UserSchema(only=("email", "password"))


@auth.post("/login")
def login():
    """Iniciar sesión"""
    load = login_schema.load(request.get_json())
    user = User.get_email(load["email"])

    if user is None or not user.check_password(load["password"]):
        raise NotAuthorizedError

    access_token = create_access_token(user)
    response = jsonify(message="Success!")
    set_access_cookies(response, access_token)
    return response


@auth.post("/signup")
def signup():
    """Registrar un nuevo usuario"""
    load = signup_schema.load(request.get_json())
    user = User(**load)
    user.save()

    return jsonify(user_schema.dump(user)), 201


@auth.get("/me")
@jwt_required()
def who_am_i():
    """Obtener datos del usuario"""
    return jsonify(user_schema.dump(current_user))


@auth.get("/protected")
@role_required("ADMINISTRATOR")
def role_protected():
    """Ruta protegida por rol de usuario"""
    return jsonify(message="You are an admin")


@auth.post("/logout")
def logout():
    """Eliminar cookies de acceso"""
    response = jsonify(message="Bye!")
    unset_access_cookies(response)
    return response
