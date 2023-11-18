"""
Inicializar ORM
"""
from typing import TypeVar, Type, List

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import select
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)
T = TypeVar("T")


class BaseModel(db.Model):
    """Clase Base para generar modelos"""

    __abstract__ = True

    def save(self):
        """Guardar instancia en db"""
        db.session.add(self)
        db.session.commit()

    def delete(self):
        """Eliminar registro de la db"""
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def get_all(cls: Type[T]) -> List[T]:
        """Devuelve una lista con todos los elementos"""
        return db.session.scalars(select(cls))
