from __future__ import annotations

import os
import sys
from pathlib import Path
from logging.config import fileConfig

from alembic import context
from sqlalchemy import engine_from_config, pool
from sqlalchemy.engine import Connection

# --- Loading .env.local -------------------------------------------------------
# Szukamy .env.local w katalogu nadrzędnym względem tego env.py (czyli w apprunner/)
BASE_DIR = Path(__file__).resolve().parents[1]
ENV_FILE = BASE_DIR / ".env.local"

if ENV_FILE.exists():
    try:
        from dotenv import load_dotenv  # python-dotenv
        load_dotenv(ENV_FILE)
    except Exception:
        # Jeśli python-dotenv nie jest zainstalowany, pomijamy – zmienne mogą być już w środowisku
        pass

# --- Python path, aby działał import "app.models" -----------------------------
# Dodajemy backend/apprunner do PYTHONPATH
if str(BASE_DIR) not in sys.path:
    sys.path.append(str(BASE_DIR))

# Import modelowej metadaty
from app.models import Base  # noqa: E402

# Alembic Config
config = context.config

# Logowanie z alembic.ini
if config.config_file_name:
    fileConfig(config.config_file_name)

# Metadata do autogeneracji
target_metadata = Base.metadata


def build_sqlalchemy_url() -> str:
    """
    Składa URL na podstawie zmiennych środowiskowych:
    DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME, DB_SSLMODE
    Korzystamy z drivera psycopg (psycopg3).
    """
    user = os.getenv("DB_USER", "")
    pwd = os.getenv("DB_PASSWORD", "")
    host = os.getenv("DB_HOST", "127.0.0.1")
    port = os.getenv("DB_PORT", "5432")
    name = os.getenv("DB_NAME", "myapp")
    sslmode = os.getenv("DB_SSLMODE", "disable")  # "disable" lokalnie, "require" dla RDS

    # Uwaga: jeśli hasło zawiera znaki specjalne, w razie potrzeby je zurl-encode’uj.
    return f"postgresql+psycopg://{user}:{pwd}@{host}:{port}/{name}?sslmode={sslmode}"


def run_migrations_offline() -> None:
    """Migracje w trybie offline."""
    url = build_sqlalchemy_url()
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,  # wykrywaj zmiany typów kolumn
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Migracje w trybie online (z aktywnym połączeniem)."""
    # Wstrzykujemy URL do configu, aby engine_from_config go użył
    sqlalchemy_section = config.get_section(config.config_ini_section) or {}
    sqlalchemy_section["sqlalchemy.url"] = build_sqlalchemy_url()

    connectable = engine_from_config(
        sqlalchemy_section,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
        future=True,
    )

    with connectable.connect() as connection:  # type: Connection
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,  # wykrywaj zmiany typów kolumn
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()