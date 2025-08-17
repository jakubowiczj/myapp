from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import String
from sqlalchemy.dialects.postgresql import JSONB

class Base(DeclarativeBase):
    pass

class Item(Base):
    __tablename__ = "items"
    pk: Mapped[str] = mapped_column(String, primary_key=True)
    body: Mapped[dict] = mapped_column(JSONB, nullable=False)
