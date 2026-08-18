from src.config import settings
from src.infrastructure.adapters.tibia_api_adapter import TibiaApiAdapter
from src.infrastructure.database.database import SessionLocal
from src.infrastructure.database.repositories.kill_statistics import KillStatisticsRepository


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
            self._tibia_api_adapter.get_kill_statistics(world)
            self._kill_statistics_repository.save()


if __name__ == '__main__':
    try:
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
