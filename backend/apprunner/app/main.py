import os
from fastapi import FastAPI, Depends, HTTPException, Body
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import text

from .database import engine, get_db
from .models import Base
from . import crud

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
def health(db: Session = Depends(get_db)):
    try:
        db.execute(text("SELECT 1"))
        return {"status": "up"}
    except Exception as e:
        return {"status": "degraded", "detail": str(e)}

# PUT przyjmuje dowolny JSON bez wrappera
@app.put("/items/{pk}")
def put_item(pk: str, body: dict = Body(default_factory=dict), db: Session = Depends(get_db)):
    out = crud.put_item(db, pk, body or {})
    return {"pk": out["pk"], "body": out["body"]}

# GET zwraca zapisany JSON w wrapperze (pk + body)
@app.get("/items/{pk}")
def get_item(pk: str, db: Session = Depends(get_db)):
    out = crud.get_item(db, pk)
    if not out:
        raise HTTPException(status_code=404, detail="Not found")
    return {"pk": out["pk"], "body": out["body"]}
