from sqlalchemy.orm import Session



class KillStatisticsRepository:
    def __init__(self, db: Session):
        self._db = db