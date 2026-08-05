from abc import ABC, abstractmethod

import requests
from requests import get


class BaseApiClient(ABC):
    """Базовый абстрактный класс для API-клиентов."""

    def __init__(self, base_url: str) -> None:
        self.base_url = base_url

    @abstractmethod
    def fetch_data(self, *args, **kwargs) -> None | list:
        """Абстрактный метод для получения и обработки данных."""
        pass


class ApiCountryCoordinates(BaseApiClient):
    """Класс для получения координат страны с 'https://nominatim.openstreetmap.org/search' в виде
    списка из 4х 'координат'"""

    def __init__(self) -> None:
        super().__init__(base_url="https://nominatim.openstreetmap.org/search")

    def fetch_data(self, country: str) -> None | list:
        """Получает координаты страны(прямоугольник) из API openstreetmap указанной страны"""
        headers = {
            "User-Agent": "test-app/1.0",
        }
        # Указываем параметры: в каком формате возвращать данные и максимальную длину списка стран в ответе.
        params = {
            "country": country,
            "format": "json",
            "limit": 1,
        }
        try:
            response = get(url=self.base_url, params=params, headers=headers, timeout=10)
            response.raise_for_status()
        except requests.RequestException as e:
            print(f"Ошибка запроса к Nominatim: {e}")
            return None
        data_country = response.json()
        if not data_country:
            print("Страна не найдена.")
            return []
        geo_coordinates = data_country[0].get("boundingbox")
        if geo_coordinates is None:
            return []
        return geo_coordinates


class ApiAeroplanesCountry(BaseApiClient):
    """Класс для получения списка самолетов с 'https://nominatim.openstreetmap.org/search'
    в пределах страны в виде словаря"""

    def __init__(self) -> None:
        super().__init__(base_url="https://opensky-network.org/api/states/all")

    def fetch_data(self, geo_coordinates: list) -> None | list[dict]:
        """Получает список самолетов нахадящихся в пределах указанных координат по API opensky-network.org"""
        if len(geo_coordinates) != 4:
            print("geo_coordinates должен содержать 4 значения: [lamin, lamax, lomin, lomax]")
            return None
        params = {
            "lamin": geo_coordinates[0],
            "lamax": geo_coordinates[1],
            "lomin": geo_coordinates[2],
            "lomax": geo_coordinates[3],
        }
        try:
            response = get(url=self.base_url, params=params, timeout=10)
            response.raise_for_status()
        except requests.RequestException as e:
            print(f"Ошибка запроса к OpenSky: {e}")
            return None
        aeroplanes = response.json()["states"]
        return aeroplanes
