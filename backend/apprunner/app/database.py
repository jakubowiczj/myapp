import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

def build_db_url() -> str:
    host = os.getenv("DB_HOST", "127.0.0.1")
    port = os.getenv("DB_PORT", "5432")
    name = os.getenv("DB_NAME", "myapp")
    user = os.getenv("DB_USER", "appuser")
    pwd  = os.getenv("DB_PASSWORD", "devpass")
    # sslmode=require jeśli łączymy się do RDS (nie localhost)
    sslmode = "require" if host not in ("127.0.0.1", "localhost") else "disable"
    return f"postgresql+psycopg://{user}:{pwd}@{host}:{port}/{name}?sslmode={sslmode}"

DATABASE_URL = build_db_url()

engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
