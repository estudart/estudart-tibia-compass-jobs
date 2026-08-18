from sqlalchemy.orm import Session

from src.infrastructure.database.tables.kill_statistics import KillStatistics



class KillStatisticsRepository:
    def __init__(self, db: Session):
        self._db = db
    
    def save(self):
        new_kill_statistics = KillStatistics()
        self._db.add(new_kill_statistics)
        return new_kill_statistics
