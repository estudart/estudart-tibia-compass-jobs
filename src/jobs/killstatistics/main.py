from src.config import settings
from src.infrastructure.adapters.tibia_api_adapter import TibiaApiAdapter



class KillStatisticsSync:
    def __init__(self) -> None:
        self._tibia_api_adapter = TibiaApiAdapter()
        self._kill_statistics_repository = ""

    def sync_db(self):
        worlds = settings.world_list

        for world in worlds:
             


if __name__ == '__main__':
    pass