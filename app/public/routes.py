from flask import send_from_directory, current_app

from . import public


@public.get("/media/<path:file_path>")
def media(file_path: str):
    """Servir archivos estáticos"""
    return send_from_directory(current_app.config["MEDIA_ROOT"], file_path)
