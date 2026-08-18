from src.infrastructure.database.database import Base

class KillStatistics(Base):
    id: Mapped[int]
    date: str
    race: str
    last_day_players_killed: int
    last_day_killed: int
    last_week_players_killed: int