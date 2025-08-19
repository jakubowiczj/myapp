from sqlalchemy import select
from sqlalchemy.orm import Session
from .models import User

def list_users(db: Session) -> list[User]:
    stmt = select(User).order_by(User.last_name, User.first_name)
    return db.execute(stmt).scalars().all()
