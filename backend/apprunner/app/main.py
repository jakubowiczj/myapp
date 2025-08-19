import os
from fastapi import FastAPI, Depends, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import text

from .database import engine, get_db
from .models import Base
from . import crud, schemas

APP_NAME = "MyApp API (SQLAlchemy + Postgres)"
ALLOWED_ORIGINS = [o.strip() for o in os.environ.get("ALLOWED_ORIGINS", "*").split(",") if o.strip()] or ["*"]

app = FastAPI(title=APP_NAME)

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)

@app.get("/health")
def health():
    return {"status": "up"}

@app.get("/ping")
def ping():
    return {"pong": True}

@app.get("/cities", response_model=list[schemas.CityOut])
def get_cities(db: Session = Depends(get_db)):
    from .models import City  # local import to avoid circular imports
    from sqlalchemy import select
    rows = db.execute(select(City).order_by(City.name)).scalars().all()
    return rows

@app.get("/work-locations", response_model=list[schemas.WorkLocationOut])
def get_work_locations(db: Session = Depends(get_db)):
    from .models import WorkLocation
    from sqlalchemy import select
    rows = db.execute(select(WorkLocation).order_by(WorkLocation.name)).scalars().all()
    return rows

@app.get("/users", response_model=list[schemas.UserOut])
def get_users(db: Session = Depends(get_db)):
    return crud.list_users(db)

@app.get("/users/table", response_model=list[schemas.UserRow], summary="List Users (flattened for table)")
def users_table(
    page: int = Query(1, ge=1),
    limit: int = Query(50, ge=1, le=200),
    sort: str = Query("last_name"),
    order: str = Query("asc"),
    db: Session = Depends(get_db),
):
    return crud.list_user_rows(db, page=page, limit=limit, sort=sort, order=order)
