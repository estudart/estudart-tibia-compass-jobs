from datetime import date

from src.config import settings
from src.infrastructure.adapters.tibia_api_adapter import TibiaApiAdapter
from src.infrastructure.database.database import SessionLocal
from src.infrastructure.database.repositories.creatures import CreaturesRepository
from src.infrastructure.database.database import engine, Base

class CreaturesSync:
    def __init__(
        self,
        tibia_api_adapter: TibiaApiAdapter,
        creatures_repository: CreaturesRepository,
    ) -> None:
        self._tibia_api_adapter = tibia_api_adapter
        self._creatures_repository = creatures_repository
    
    

    def sync_db(self):
        try:
            print("Calling api...")
            creatures = self._tibia_api_adapter.get_creatures()
            boosted_creature = creatures["boosted"]
            new_creature = self._creatures_repository.save(
                world,
                creature["name"],
                creature["race"],
                creature["image_url"],
                creature["featured"],
                True,
                date.today()
            )
            print(f"New creature saved: {new_creature}")

            for creature in creatures["creature_list"]:
                new_creature = self._creatures_repository.save(
                    world,
                    creature["name"],
                    creature["race"],
                    creature["image_url"],
                    creature["featured"],
                    False,
                    date.today()
                )
                print(f"New creature saved: {new_creature}")
        except Exception as err:
            print(f"[ERROR] Could not sync data, reason: {err}")

def create_tables():
    print("Creating tables in PostgreSQL...")
    # This reads all classes inheriting from Base and creates them if they don't exist
    Base.metadata.create_all(bind=engine)
    print("Tables created successfully!")

if __name__ == '__main__':
    try:
        create_tables()

        tibia_api_adapter = TibiaApiAdapter()
        db_session = SessionLocal()
        creatures_repository = CreaturesRepository(db=db_session)

        service = CreaturesSync(
            tibia_api_adapter=tibia_api_adapter,
            creatures_repository=creatures_repository
        )

        service.sync_db()
    except Exception as err:
        print(f"Could not run sync, reason: {err}")
