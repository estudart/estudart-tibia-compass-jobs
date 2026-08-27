from datetime import datetime

from sqlalchemy import (
    Boolean,
    ForeignKey,
    Integer,
    String
)
from sqlalchemy.orm import Mapped, mapped_column

from src.infrastructure.database.database import Base

class KillStatistics(Base):
    __tablename__ = "kill_statistics"

    id: Mapped[int] = mapped_column(primary_key=True)
    world: Mapped[str] = mapped_column(String, default="")
    race: Mapped[str] = mapped_column(String, default="")
    last_day_players_killed: Mapped[int] = mapped_column(Integer, default=0)
    last_day_killed: Mapped[int] = mapped_column(Integer, default=0)
    last_week_players_killed: Mapped[int] = mapped_column(Integer, default=0)
    last_week_killed: Mapped[int] = mapped_column(Integer, default=0)
    date: Mapped[datetime] = mapped_column(default=None)

    def __repr__(self) -> str:
        return f"KillStatistics(id={self.id}, world={self.world!r}, race={self.race!r}, last_day_killed={self.last_day_killed})"
