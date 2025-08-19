import os
from logging.config import fileConfig
from sqlalchemy import create_engine, pool
from alembic import context
from dotenv import load_dotenv
from app.models import Base

config = context.config
if config.config_file_name:
    fileConfig(config.config_file_name)

load_dotenv(os.path.join(os.path.dirname(__file__), "..", ".env.local"))

driver = os.getenv("DB_DRIVER", "postgresql+psycopg")
user = os.getenv("DB_USER", "")
password = os.getenv("DB_PASSWORD", "")
host = os.getenv("DB_HOST", "127.0.0.1")
port = os.getenv("DB_PORT", "5432")
name = os.getenv("DB_NAME", "")
sslmode = os.getenv("DB_SSLMODE", "disable")

database_url = f"{driver}://{user}:{password}@{host}:{port}/{name}"
if sslmode and sslmode != "disable":
    sep = "&" if "?" in database_url else "?"
    database_url = f"{database_url}{sep}sslmode={sslmode}"

target_metadata = Base.metadata

def run_migrations_offline():
    context.configure(
        url=database_url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,
    )
    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    connectable = create_engine(database_url, poolclass=pool.NullPool)
    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
        )
        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
