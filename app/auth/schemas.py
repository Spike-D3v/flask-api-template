from marshmallow import fields as f

from app.extensions import ma


class RoleSchema(ma.Schema):
    """Representa un rol de usuario"""

    name = f.String()
    title = f.String()
    description = f.String()
    created_at = f.DateTime(format="%Y-%m-%d", data_key="createdAt", dump_only=True)
    updated_at = f.DateTime(format="%Y-%m-%d", data_key="updatedAt", dump_only=True)


class UserSchema(ma.Schema):
    """Representa un usuario"""

    id = f.UUID()
    email = f.Email()
    password = f.String(load_only=True)
    is_active = f.Boolean(data_key="isActive")
    roles = f.List(f.Pluck(RoleSchema, "name"))
    created_at = f.DateTime(format="%Y-%m-%d", data_key="createdAt", dump_only=True)
    updated_at = f.DateTime(format="%Y-%m-%d", data_key="updatedAt", dump_only=True)


class LoginSchema(ma.Schema):
    """Representa una solicitud de inicio de sesión"""

    email = f.Email(required=True)
    password = f.String(required=True, load_only=True)
