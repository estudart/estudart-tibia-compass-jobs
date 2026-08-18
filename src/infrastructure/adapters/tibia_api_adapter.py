import requests



class TibiaApiAdapter:
    def __init__(self):
        self._session = requests.Session()
        self._url = "https://api.tibiadata.com"

    def get_creatures(self):
        url = f"{self._url}/v4/creatures"
        response = self._session.get(url=url)
        response_json = response.json()
        return response_json

    def get_kill_statistics(self, world: str):
        url = f"{self._url}/v4/killstatistics/{world}"
        response = self._session.get(url=url)
        response_json = response.json()
        return response_json["killstatistics"]["entries"]

    def get_house(self, world: str, town: str):
        url = f"{self._url}/v4/houses/{world}/{town}"
        response = self._session.get(url=url)
        response_json = response.json()
        return response_json

