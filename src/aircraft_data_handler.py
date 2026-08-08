from typing import Any


class Aeroplane:
    def __init__(
        self,
        callsign: str | None = None,
        country: str | None = None,
        velocity: float | None = None,
        altitude: float | None = None,
    ):
        """
        Класс, представляющий самолёт по данным OpenSky Network.

        Особенности:
            - callsign нормализуется: удаляются пробелы по краям; если пусто — ставится "No callsign".
            - country нормализуется аналогично; если пусто — "None country".
            - velocity должен быть неотрицательным числом; иначе ValueError.
            - в altitude может приходить отрицательным из API; отрицательные значения приводятся к 0.
        """
        if callsign is None:
            callsign = ""
        if not isinstance(callsign, str):
            raise ValueError("callsign должен быть строкой")
        callsign = callsign.strip()
        self.callsign = callsign if callsign else "No callsign"

        if country is None:
            country = ""
        if not isinstance(country, str):
            raise ValueError("country должен быть строкой")
        country = country.strip()
        self.country = country if country else "None country"

        if velocity is None:
            velocity = 0
        if not isinstance(velocity, (int, float)):
            raise ValueError(f"velocity должен быть числом, а не {type(velocity).__name__}")
        elif velocity < 0:
            raise ValueError("velocity должен быть неотрицательным числом")
        self.velocity = float(velocity)

        if altitude is None:
            altitude = 0
        if not isinstance(altitude, (int, float)):
            raise ValueError(f"altitude должен быть числом, а не {type(altitude).__name__}")
        # В данных opensky-network.org бывает отрицательня высота, выравниваем ее в 0
        if altitude < 0:
            altitude = 0
        self.altitude = altitude

    @classmethod
    def cast_to_object_list(cls, country_aeroplanes: list[dict]) -> list[Aeroplane]:
        """Создает из списка словарей список объектов Aeroplane"""
        aeroplane_list = []
        for aeroplane in country_aeroplanes:
            callsign = aeroplane[1]
            country = aeroplane[2]
            velocity = aeroplane[9]
            altitude = aeroplane[7]
            # удаляем лишние пробелы и приводем к строке
            callsign_str = str(callsign).strip() if callsign is not None else ""
            country_str = str(country).strip() if country is not None else ""

            single_aeroplane = cls(callsign_str, country_str, velocity, altitude)
            aeroplane_list.append(single_aeroplane)
        return aeroplane_list

    def __eq__(self, other: object) -> bool:
        """Равенство объектов (сравнение самолетов между собой по скорости и высоте)"""
        if not isinstance(other, Aeroplane):
            raise TypeError
        return self.velocity == other.velocity and self.altitude == other.altitude

    def __gt__(self, other: object) -> Any | bool:
        """Больше (сравнение самолетов между собой по скорости и высоте)"""
        if not isinstance(other, Aeroplane):
            raise TypeError
        if self.velocity != other.velocity:
            return self.velocity > other.velocity
        return self.altitude > other.altitude

    def __lt__(self, other: object) -> Any | bool:
        """Меньше (сравнение самолетов между собой по скорости и высоте)"""
        if not isinstance(other, Aeroplane):
            raise TypeError
        if self.velocity != other.velocity:
            return self.velocity < other.velocity
        return self.altitude < other.altitude

    def __str__(self) -> str:
        """Для отображение информации о самолете в строковом виде"""
        return (
            f"Aeroplane(callsign={self.callsign!r}, country={self.country!r}, "
            f"velocity={self.velocity}, altitude={self.altitude})"
        )

    def to_dict(self) -> dict:
        """Преобразование в словарь"""
        return {
            "callsign": self.callsign,
            "country": self.country,
            "velocity": self.velocity,
            "altitude": self.altitude,
        }
