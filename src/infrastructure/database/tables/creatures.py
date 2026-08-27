from datetime import datetime

from sqlalchemy import (
    Boolean,
    ForeignKey,
    Integer,
    String
)
from sqlalchemy.orm import Mapped, mapped_column

from src.infrastructure.database.database import Base

class Creatures(Base):
    __tablename__ = "creatures"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String, default="")
    race: Mapped[str] = mapped_column(String, default="")
    image_url: Mapped[str] = mapped_column(String, default="")
    featured: Mapped[bool] = mapped_column(Boolean, default=False)
    boosted: Mapped[bool] = mapped_column(Boolean, default=False)
    date: Mapped[datetime] = mapped_column(default=None)
