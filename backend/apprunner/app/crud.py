from sqlalchemy.orm import Session
from sqlalchemy import asc, desc, select
from .models import User, City, WorkLocation
from .schemas import UserRow

ALLOWED_SORT_FIELDS = {
    "first_name": User.first_name,
    "last_name": User.last_name,
    "email": User.email,
    "job_title": User.job_title,
    "status": User.status,
    "created_at": User.created_at,
    "updated_at": User.updated_at,
}

def list_users(db: Session) -> list[User]:
    stmt = select(User).order_by(User.last_name, User.first_name)
    return db.execute(stmt).scalars().all()

def list_user_rows(
    db: Session,
    page: int = 1,
    limit: int = 50,
    sort: str = "last_name",
    order: str = "asc",
) -> list[UserRow]:
    if page < 1:
        page = 1
    if limit < 1 or limit > 200:
        limit = 50

    sort_col = ALLOWED_SORT_FIELDS.get(sort, User.last_name)
    sorter = asc(sort_col) if order.lower() != "desc" else desc(sort_col)

    q = (
        db.query(
            User.id,
            User.first_name,
            User.last_name,
            User.email,
            User.job_title,
            User.avatar_url,
            User.status,
            City.name.label("city_name"),
            WorkLocation.name.label("work_location_name"),
            User.created_at,
            User.updated_at,
        )
        .join(City, User.city_id == City.id)
        .join(WorkLocation, User.work_location_id == WorkLocation.id)
        .order_by(sorter)
        .offset((page - 1) * limit)
        .limit(limit)
    )

    rows = []
    for r in q.all():
        rows.append(
            UserRow(
                id=str(r.id),
                first_name=r.first_name,
                last_name=r.last_name,
                email=r.email,
                job_title=r.job_title,
                avatar_url=r.avatar_url,
                status=r.status.value,  # Corrected
                city_name=r.city_name,
                work_location_name=r.work_location_name,
                created_at=r.created_at,
                updated_at=r.updated_at,
            )
        )
    return rows
