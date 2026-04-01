from datetime import datetime
from uuid import UUID as PythonUUID, uuid4
from typing import Optional, TYPE_CHECKING
from .db_models import Base
from sqlalchemy import String, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID as SQLAlchemyUUID
from sqlalchemy.orm import Mapped, mapped_column, relationship


if TYPE_CHECKING:
    from app.models.auth_model import User


class Todo(Base):

    """"Todo table"""

    __tablename__ = "todo"

    id: Mapped[PythonUUID] = mapped_column(SQLAlchemyUUID(as_uuid=True), primary_key=True, default=uuid4)
    owner_id: Mapped[PythonUUID] = mapped_column(
        SQLAlchemyUUID(as_uuid=True),
        ForeignKey("users.id"),
        nullable=False,
    )
    title: Mapped[Optional[str]] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(String(255), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, nullable=False, onupdate=datetime.now)

    owner: Mapped["User"] = relationship(back_populates="todos")
