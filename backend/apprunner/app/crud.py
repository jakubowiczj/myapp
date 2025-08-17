from sqlalchemy.orm import Session
from sqlalchemy import select
from .models import Item

def put_item(db: Session, pk: str, body: dict) -> dict:
    obj = db.get(Item, pk)
    if obj is None:
        obj = Item(pk=pk, body=body)
        db.add(obj)
    else:
        obj.body = body
    db.commit()
    db.refresh(obj)
    return {"pk": obj.pk, "body": obj.body}

def get_item(db: Session, pk: str) -> dict | None:
    obj = db.get(Item, pk)
    if obj is None:
        return None
    return {"pk": obj.pk, "body": obj.body}
