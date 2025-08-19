import os
import uuid
from sqlalchemy import create_engine, text

# env
user = os.getenv("DB_USER", "appuser")
password = os.getenv("DB_PASSWORD", "devpass")
host = os.getenv("DB_HOST", "127.0.0.1")
port = os.getenv("DB_PORT", "5432")
name = os.getenv("DB_NAME", "myapp")
sslmode = os.getenv("DB_SSLMODE", "disable")

url = f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{name}"
if sslmode != "disable":
    url += f"?sslmode={sslmode}"

engine = create_engine(url, echo=True, future=True)

with engine.begin() as conn:
    # Cities
    conn.execute(text("""
        INSERT INTO cities (id, name) VALUES
        (:id1, 'Warsaw'),
        (:id2, 'Krakow')
        ON CONFLICT (name) DO NOTHING
    """), dict(id1=str(uuid.uuid4()), id2=str(uuid.uuid4())))

    # Work locations
    conn.execute(text("""
        INSERT INTO work_locations (id, name) VALUES
        (:id1, 'HQ'),
        (:id2, 'Remote')
        ON CONFLICT (name) DO NOTHING
    """), dict(id1=str(uuid.uuid4()), id2=str(uuid.uuid4())))

    # Users
    # Pobierz city_id + work_location_id
    city_id = conn.execute(text("SELECT id FROM cities WHERE name='Warsaw'")).scalar_one()
    wl_id = conn.execute(text("SELECT id FROM work_locations WHERE name='HQ'")).scalar_one()

    conn.execute(text("""
        INSERT INTO users (id, first_name, last_name, email, job_title, status, city_id, work_location_id)
        VALUES
        (:id1, 'Jan', 'Kowalski', 'jan.kowalski@example.com', 'Engineer', 'active', :city, :wl),
        (:id2, 'Anna', 'Nowak', 'anna.nowak@example.com', 'Manager', 'active', :city, :wl)
        ON CONFLICT (email) DO NOTHING
    """), dict(
        id1=str(uuid.uuid4()),
        id2=str(uuid.uuid4()),
        city=city_id,
        wl=wl_id,
    ))

print("✅ Seed completed")