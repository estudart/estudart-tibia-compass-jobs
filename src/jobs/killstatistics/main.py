from datetime import date

from src.config import settings
from src.infrastructure.adapters.tibia_api_adapter import TibiaApiAdapter
from src.infrastructure.database.database import SessionLocal
from src.infrastructure.database.repositories.kill_statistics import KillStatisticsRepository
from src.infrastructure.database.database import engine, Base

class KillStatisticsSync:
    def __init__(
        self,
        tibia_api_adapter: TibiaApiAdapter,
        kill_statistics_repository: KillStatisticsRepository,
    ) -> None:
        self._tibia_api_adapter = tibia_api_adapter
        self._kill_statistics_repository = kill_statistics_repository

    def sync_db(self):
        worlds = settings.world_list

        for world in worlds:
            try:
                print("Calling api...")
                statistics = self._tibia_api_adapter.get_kill_statistics(world)
                for statistic in statistics:
                    new_statistic = self._kill_statistics_repository.save(
                        world,
                        statistic["race"],
                        statistic["last_day_players_killed"],
                        statistic["last_day_killed"],
                        statistic["last_week_players_killed"],
                        statistic["last_week_killed"],
                        date.today()
                    )
                    print(f"New stats saved: {new_statistic}")
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
        kill_statistics_repository = KillStatisticsRepository(db=db_session)

        service = KillStatisticsSync(
            tibia_api_adapter=tibia_api_adapter,
            kill_statistics_repository=kill_statistics_repository
        )

        service.sync_db()
    except Exception as err:
        print(f"Could not run sync, reason: {err}")
