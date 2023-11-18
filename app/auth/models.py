from datetime import datetime
from typing import Optional, List
from uuid import uuid4, UUID

import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column, relationship
from werkzeug.security import generate_password_hash, check_password_hash

from app.core.exceptions import NotAuthorizedError
from app.db import BaseModel, db
from app.extensions import jwt


class Role(BaseModel):
    """Representa el rol de un usuario"""

    __tablename__ = "auth_role"

    id: Mapped[UUID] = mapped_column(sa.UUID, primary_key=True, default=uuid4)
    name: Mapped[str] = mapped_column(sa.String, nullable=False, unique=True)
    title: Mapped[Optional[str]] = mapped_column(sa.String)
    description: Mapped[Optional[str]] = mapped_column(sa.String)
    created_at: Mapped[datetime] = mapped_column(
        sa.DateTime, nullable=False, default=datetime.now
    )
    updated_at: Mapped[Optional[datetime]] = mapped_column(
        sa.DateTime, onupdate=datetime.now
    )

    @classmethod
    def get_id(cls, id: str | UUID) -> Optional["Role"]:
        """Devuelve el rol con el ID o ``None``"""
        stmt = sa.select(cls).where(cls.id == id)
        return db.session.scalar(stmt)

    @classmethod
    def get_name(cls, name: str) -> Optional["Role"]:
        """Devuelve el rol con el nombre o ``None``"""
        stmt = sa.select(cls).where(cls.name == name)
        return db.session.scalar(stmt)


user_role = db.Table(
    "auth_user_role",
    sa.Column("user_id", sa.UUID, sa.ForeignKey("auth_user.id"), primary_key=True),
    sa.Column("role_id", sa.UUID, sa.ForeignKey("auth_role.id"), primary_key=True),
)


class User(BaseModel):
    """Representa un usuario del sistema"""

    __tablename__ = "auth_user"

    id: Mapped[UUID] = mapped_column(sa.UUID, primary_key=True, default=uuid4)
    email: Mapped[str] = mapped_column(sa.String, nullable=False, unique=True)
    password: Mapped[str] = mapped_column(sa.String, nullable=False)
    is_active: Mapped[bool] = mapped_column(sa.Boolean, nullable=False, default=True)
    created_at: Mapped[datetime] = mapped_column(
        sa.DateTime, nullable=False, default=datetime.now
    )
    updated_at: Mapped[Optional[datetime]] = mapped_column(
        sa.DateTime, onupdate=datetime.now
    )

    roles: Mapped[List[Role]] = relationship(Role, secondary=user_role)

    def save(self, set_password=True):
        if set_password:
            self.set_password(self.password)
        super().save()

    def set_password(self, password: str) -> None:
        self.password = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password, password)

    @classmethod
    def get_id(cls, id: str | UUID) -> Optional["User"]:
        """Devuelve el usuario con el ID o ``None``"""
        stmt = sa.select(cls).where(cls.id == id)
        return db.session.scalar(stmt)

    @classmethod
    def get_email(cls, email: str) -> Optional["User"]:
        """Devuelve el usuario con el email o ``None``"""
        stmt = sa.select(cls).where(cls.email == email)
        return db.session.scalar(stmt)


@jwt.user_identity_loader
def user_identity_lookup(user: User):
    return user.id


@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data) -> User:
    identity = jwt_data["sub"]
    user = User.get_id(identity)
    if user is None:
        raise NotAuthorizedError
    return user
