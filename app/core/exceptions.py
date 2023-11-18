class BaseApiError(Exception):
    """Error inesperado"""

    status_code = 500
    message = "Unexpected server error"

    def __init__(
        self, message: str = None, status_code: int = None, payload: dict = None, *args
    ):
        """Reportar error inesperado"""
        if message is not None:
            self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload or {}
        super().__init__(self.message, *args)

    def to_dict(self) -> dict:
        """Genera un diccionario con el mensaje y payload del error"""
        data = self.payload
        data["message"] = self.message
        return data


class NotAuthorizedError(BaseApiError):
    """El usuario no tiene acceso a un recurso"""

    status_code = 401
    message = "Not authorized"


class PermissionsError(BaseApiError):
    """El usuario no tiene suficientes permisos para acceder al recurso"""

    status_code = 403
    message = "Access denied"


class NotFoundError(BaseApiError):
    """No se reconoce el recurso solicitado"""

    status_code = 404
    message = "Resource not found"


class BadRequestError(BaseApiError):
    """La solicitud está mal formada"""

    status_code = 400
    message = "Missing required fields or parameters"
