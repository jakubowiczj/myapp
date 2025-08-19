from datetime import datetime
from pydantic import BaseModel, EmailStr
from uuid import UUID
from typing import Optional

class CityOut(BaseModel):
    id: UUID
    name: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class WorkLocationOut(BaseModel):
    id: UUID
    name: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class UserOut(BaseModel):
    id: UUID
    first_name: str
    last_name: str
    email: EmailStr
    job_title: str | None = None
    avatar_url: str | None = None
    status: str
    city_id: UUID
    work_location_id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class UserRow(BaseModel):
    id: str
    first_name: str
    last_name: str
    email: EmailStr
    job_title: Optional[str] = None
    avatar_url: Optional[str] = None
    status: str
    city_name: str
    work_location_name: str
    created_at: datetime
    updated_at: datetime
