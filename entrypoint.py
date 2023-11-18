"""
Generar una instancia de la aplicación
"""
import os

from app import create_app

settings = os.getenv("APP_SETTINGS_MODULE")
app = create_app(settings)
