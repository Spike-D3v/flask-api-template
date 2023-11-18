from functools import wraps

from flask_jwt_extended import verify_jwt_in_request, current_user

from app.core.exceptions import PermissionsError


def role_required(*names):
    """Permitir el acceso a usuarios con los roles"""

    def wrapper(view_func):
        @wraps(view_func)
        def decorator(*args, **kwargs):
            verify_jwt_in_request()
            user_roles = [role.name for role in current_user.roles]
            if any(role_name not in user_roles for role_name in names):
                raise PermissionsError
            return view_func(*args, **kwargs)

        return decorator

    return wrapper
