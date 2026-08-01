from unittest import result


class Aeroplane:
    def __init__(self, callsign=None, country=None, velocity=None, altitude=None):
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
        self.velocity = velocity

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
        """Создает из списка словарей списоб объектов Aeroplane"""
        aeroplane_list = []
        for aeroplane in country_aeroplanes:
            callsign = aeroplane[1].strip()  # удаляем пробелы(с сервиса всегда идет 8 символов, добивают пробелами)
            country = aeroplane[2]
            velocity = aeroplane[9]
            altitude = aeroplane[7]
            single_aeroplane = Aeroplane(callsign, country, velocity, altitude)
            aeroplane_list.append(single_aeroplane)
        return aeroplane_list

    def __eq__(self, other):
        """Равенство объектов (сравнение самолетов между собой по скорости и высоте)"""
        if not isinstance(other, Aeroplane):
            raise TypeError
        if self.velocity == other.velocity and self.altitude == other.altitude:
            return True
        return False

    def __gt__(self, other):
        """Больше (сравнение самолетов между собой по скорости и высоте)"""
        if not isinstance(other, Aeroplane):
            raise TypeError
        if self.velocity > other.velocity:
            return True
        if self.altitude > other.altitude:
            return True
        return False

    def __lt__(self, other):
        """Меньше (сравнение самолетов между собой по скорости и высоте)"""
        if not isinstance(other, Aeroplane):
            raise TypeError
        if self.velocity < other.velocity:
            return True
        if self.altitude < other.altitude:
            return True
        return False

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
