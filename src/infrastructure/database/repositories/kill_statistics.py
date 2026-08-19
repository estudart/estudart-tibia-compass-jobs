from datetime import datetime

from sqlalchemy.orm import Session

from src.infrastructure.database.tables.kill_statistics import KillStatistics



class KillStatisticsRepository:
    def __init__(self, db: Session):
        self._db = db
    
    def save(
        self,
        race: str,
        last_day_players_killed: int,
        last_day_killed: int,
        last_week_players_killed: int,
        last_week_killed: int,
        date: datetime
    ) -> KillStatistics:
        new_kill_statistics = KillStatistics(
            race=race,
            last_day_players_killed=last_day_players_killed,
            last_day_killed=last_day_killed,
            last_week_players_killed=last_week_players_killed,
            last_week_killed=last_week_killed,
            date=date
        )
        self._db.add(new_kill_statistics)
        self._db.commit()
        return new_kill_statistics
