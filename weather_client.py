import requests
import json


class WeatherClient:
    _BASE_URL = "https://www.metaweather.com/api"
    _LOCATION_SEARCH_QUERY = "/api/location/search/?query={query}"
    _LOCATION_INFO = "/api/location/{location_id}/"

    def __init__(self):
        pass

    def get_locations(self, location_query):
        res = requests.get(
            "/".join(
                [
                    self._BASE_URL,
                    self._LOCATION_SEARCH_QUERY.format(query=location_query),
                ]
            )
        )
        res.raise_for_status()

        return json.loads(res.content)

    def get_weather(self, location_id):
        res = requests.get(
            "/".join(
                [self._BASE_URL, self._LOCATION_INFO.format(location_id=location_id)]
            )
        )
        res.raise_for_status()

        return json.loads(res.content)


if __name__ == "__main__":
    client = WeatherClient()
    locations = client.get_locations("Moscow")
    weather = client.get_weather(locations[0]["woeid"])
    print(json.dumps(weather, indent=2))
