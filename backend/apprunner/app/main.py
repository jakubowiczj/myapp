import os, json
import psycopg
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

APP_NAME = "MyApp API (App Runner/EB + Postgres)"

DB_HOST = os.environ.get("DB_HOST", "")
DB_PORT = int(os.environ.get("DB_PORT", "5432"))
DB_NAME = os.environ.get("DB_NAME", "")
DB_USER = os.environ.get("DB_USER", "")
DB_PASSWORD = os.environ.get("DB_PASSWORD", "")

ALLOWED_ORIGINS = [o.strip() for o in os.environ.get("ALLOWED_ORIGINS", "*").split(",") if o.strip()] or ["*"]

app = FastAPI(title=APP_NAME)

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def dsn() -> str:
    if not (DB_HOST and DB_NAME and DB_USER and DB_PASSWORD):
        raise RuntimeError("DB env vars are not set (DB_HOST, DB_NAME, DB_USER, DB_PASSWORD)")
    return (
        f"host={DB_HOST} port={DB_PORT} dbname={DB_NAME} user={DB_USER} "
        f"password={DB_PASSWORD} sslmode=require connect_timeout=3"
    )

def ensure_schema():
    with psycopg.connect(dsn(), autocommit=True) as conn:
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS items (
                  pk   text PRIMARY KEY,
                  body jsonb NOT NULL
                );
            """)

@app.on_event("startup")
def on_startup():
    try:
        ensure_schema()
        print("[startup] schema ensured", flush=True)
    except Exception as e:
        print(f"[startup] ensure_schema skipped: {e}", flush=True)

@app.get("/health")
def health():
    try:
        with psycopg.connect(dsn()) as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT 1")
        return {"status": "up"}
    except Exception as e:
        return {"status": "degraded", "detail": str(e)}

@app.put("/items/{pk}")
def put_item(pk: str, body: dict | None = None):
    if body is None:
        body = {}
    with psycopg.connect(dsn(), autocommit=True) as conn:
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO items (pk, body) VALUES (%s, %s::jsonb) "
                "ON CONFLICT (pk) DO UPDATE SET body = EXCLUDED.body",
                (pk, json.dumps(body)),
            )
    return {"ok": True, "item": {"pk": pk, **body}}

@app.get("/items/{pk}")
def get_item(pk: str):
    with psycopg.connect(dsn()) as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT body FROM items WHERE pk = %s", (pk,))
            row = cur.fetchone()
            if not row:
                raise HTTPException(status_code=404, detail="Not found")
            val = row[0]
            # psycopg3 może zwrócić dict, str, bytes, memoryview
            if isinstance(val, dict):
                return val
            if isinstance(val, memoryview):
                return json.loads(val.tobytes().decode("utf-8"))
            if isinstance(val, (bytes, bytearray)):
                return json.loads(val.decode("utf-8"))
            if isinstance(val, str):
                return json.loads(val)
            # fallback – spróbuj zrzutować do str i wczytać
            try:
                return json.loads(str(val))
            except Exception:
                # jako ostatnia deska – zwróć jak jest
                return val
