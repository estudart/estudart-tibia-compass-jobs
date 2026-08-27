from datetime import datetime

from sqlalchemy.orm import Session

from src.infrastructure.database.tables.creatures import Creatures

class CreaturesRepository:
    def __init__(self, db: Session):
        self._db = db

    def save(
        self,
        name: str,
        race: str,
        image_url: str,
        featured: bool,
        boosted: bool,
        date: datetime
    ) -> Creatures:
        new_creature = Creatures(
            name=name,
            race=race,
            image_url=image_url,
            featured=featured,
            boosted=boosted,
            date=date
        )
        self._db.add(new_creature)
        self._db.commit()
        return new_creature