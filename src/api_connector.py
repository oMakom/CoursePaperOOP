from abc import ABC, abstractmethod

from requests import get


class BaseApiClient(ABC):
    @abstractmethod
    def __init__(self, base_url: str) -> None:
        self.base_url = base_url


class ApiCountyCoordinates(BaseApiClient):
    """Класс для получения координат страны с 'https://nominatim.openstreetmap.org/search' в виде
    списка из 4х 'координат'"""

    def __init__(self) -> None:
        super().__init__(base_url="https://nominatim.openstreetmap.org/search")
        self.geo_coordinates = None

    def get_coordinates(self, country: str) -> None:
        headers = {
            "User-Agent": "test-app/1.0",
        }
        # Указываем параметры: в каком формате возвращать данные и максимальную длину списка стран в ответе.
        params = {
            "country": country,
            "format": "json",
            "limit": 1,
        }

        response = get(url=self.base_url, params=params, headers=headers)
        if not response.ok:  # ok == True только для 200–399
            print("Ошибка:", response.status_code, response.reason)
            print("Тело ответа:", response.text)
            return None
        else:
            data_country = response.json()
            self.geo_coordinates = data_country[0].get("boundingbox")
            return self.geo_coordinates


class ApiAeroplanesCounty(BaseApiClient):
    """Класс для получения списка самолетов с 'https://nominatim.openstreetmap.org/search'
    в пределах страны в виде словаря"""

    def __init__(self) -> None:
        super().__init__(base_url="https://opensky-network.org/api/states/all")
        self.aeroplanes = None

    def get_aeroplanes(self, geo_coordinates: list) -> None | list[list]:
        if len(geo_coordinates) != 4:
            print("geo_coordinates должен содержать 4 значения: [lamin, lamax, lomin, lomax]")
            return None
        params = {
            "lamin": geo_coordinates[0],
            "lamax": geo_coordinates[1],
            "lomin": geo_coordinates[2],
            "lomax": geo_coordinates[3],
        }

        response = get(url=self.base_url, params=params)
        if not response.ok:  # ok == True только для 200–399
            print("Ошибка:", response.status_code, response.reason)
            print("Тело ответа:", response.text)
            return None
        else:
            self.aeroplanes = response.json()['states']
            return self.aeroplanes


if __name__ == "__main__":
    api = ApiCountyCoordinates()
    api.get_coordinates("RUSSIA")
    api_Aeroplanes = ApiAeroplanesCounty()
    api_Aeroplanes.get_aeroplanes(api.geo_coordinates)
    print(api_Aeroplanes.aeroplanes)
