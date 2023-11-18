# Plantilla para api rest con Flask

Estructura inicial para desarrollar api rest con Flask, SQLAlchemy y JWT

### Instalar dependencias

```sh
pip install flask flask-sqlalchemy flask-migrate flask-marshmallow marshmallow-sqlalchemy flask-jwt-extended flask-cors
```

### Dependencias de Desarrollo

```sh
pip install pytest black flake8
```

### Setup

Crear directorios para medios y logs

```sh
mkdir media logs
```

Ajustar configuración de base de datos en `instance/config.py`

```python
SQLALCHEMY_DATABASE_URI = "dialect+connector://dbuser:dbpassword@localhost:5432/dbname"
```

### Run dev

```sh
export FLASK_APP=entrypoint:app
export APP_SETTINGS_MODULE=config.local
flask run --debug
```
