from uuid import uuid4

import pytest
from sqlalchemy import select

from app.auth.models import Role, User
from app.db import db


def create_role(name: str, **values):
    defaults = {
        "name": name,
        "title": None,
        "description": None,
    }
    defaults.update(values)
    role = Role(**defaults)
    role.save()
    return role


def create_user(email="example@mail.com", password="1234", **kwargs):
    defaults = {
        "email": email,
        "password": password,
    }
    defaults.update(kwargs)
    user = User(**defaults)
    user.save()
    return user


class TestRoleModel:
    def test_unique_name(self, app):
        with app.app_context():
            create_role("ADMINISTRATOR")
            with pytest.raises(Exception):
                create_role("ADMINISTRATOR")

            db.session.rollback()
            assert len(list(Role.get_all())) == 1

    def test_get_name(self, app):
        with app.app_context():
            create_role("ADMIN")
            role = Role.get_name("ADMIN")
            assert role is not None
            assert role.name == "ADMIN"

    def test_get_id(self, app):
        role_id = uuid4()
        with app.app_context():
            create_role("ADMIN", id=role_id)
            role = Role.get_id(role_id)
            assert role is not None
            assert role.id == role_id
            assert role.name == "ADMIN"


class TestUserModel:
    def test_unique_email(self, app):
        with app.app_context():
            create_user()
            with pytest.raises(Exception):
                create_user()

            db.session.rollback()
            assert len(list(User.get_all())) == 1

    def test_password_hash(self, app):
        with app.app_context():
            user = create_user(password="1234")

            stmt = select(User).where(User.id == user.id)
            query = db.session.scalar(stmt)

            assert query.password != "1234"

    def test_check_password(self, app):
        with app.app_context():
            user = create_user(password="1234")

            stmt = select(User).where(User.id == user.id)
            query = db.session.scalar(stmt)

            assert query.check_password("1234") is True

    def test_get_email(self, app):
        with app.app_context():
            create_user(email="example@mail.com")

            user = User.get_email("example@mail.com")
            assert user is not None
            assert user.email == "example@mail.com"

    def test_get_id(self, app):
        with app.app_context():
            user_id = uuid4()
            create_user(id=user_id)

            user = User.get_id(user_id)
            assert user is not None
            assert user.id == user_id

    def test_user_roles(self, app):
        with app.app_context():
            role = create_role("ADMIN")
            create_user(roles=[role], email="admin@example.com")

            stmt = select(User).where(User.email == "admin@example.com")
            query = db.session.scalar(stmt)

            assert role in query.roles


class TestAuth:
    def test_login(self, app, client):
        with app.app_context():
            create_user(email="foo@bar.com", password="abcd")

            body = {"email": "foo@bar.com", "password": "abcd"}

            resp = client.post("/login", json=body)

            assert resp.status_code == 200

            cookies = resp.headers.getlist("Set-Cookie")
            assert any(
                app.config["JWT_ACCESS_COOKIE_NAME"] in cookie for cookie in cookies
            )
            assert any(
                app.config["JWT_ACCESS_CSRF_COOKIE_NAME"] in cookie
                for cookie in cookies
            )

    def test_identity_lookup(self, app, client):
        with app.app_context():
            user = create_user(email="foo@bar.com", password="abcd")

            unauthenticated_resp = client.get("/me")
            assert unauthenticated_resp.status_code == 401

            with client.session_transaction():
                body = {"email": "foo@bar.com", "password": "abcd"}

                client.post("/login", json=body)
                resp = client.get("/me")

                assert resp.status_code == 200
                assert resp.json["id"] == str(user.id)
                assert resp.json["email"] == "foo@bar.com"

    def test_role_protection(self, app, client):
        with app.app_context():
            admin_role = create_role("ADMINISTRATOR")
            create_user(email="foo@bar.com", password="abcd", roles=[admin_role])

            guest_role = create_role("GUEST")
            create_user(email="guest@example.com", password="1234", roles=[guest_role])

            unauthenticated_resp = client.get("protected")
            assert unauthenticated_resp.status_code == 401

            with client.session_transaction():
                body = {"email": "foo@bar.com", "password": "abcd"}
                client.post("/login", json=body)
                admin_resp = client.get("/protected")

                assert admin_resp.status_code == 200

            with client.session_transaction():
                body = {"email": "guest@example.com", "password": "1234"}
                client.post("/login", json=body)
                guest_resp = client.get("/protected")

                assert guest_resp.status_code == 403
