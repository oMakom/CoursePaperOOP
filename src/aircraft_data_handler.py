from unittest import result


class Aeroplane:
    def __init__(self, callsign = None,country = None, velocity = None,altitude =None ):
        if not isinstance(callsign, str):
            raise ValueError("callsign должен быть строкой")
        if not callsign.strip() or callsign is None:
            callsign = "None callsign"
        self.callsign = callsign

        if not isinstance(country, str):
            raise ValueError("country должен быть строкой")
        if not country.strip() or country is None:
            country = "None callsign"
        self.country = country

        if velocity is None:
            velocity = 0
        if not isinstance(velocity, (int, float)) or velocity < 0:
            raise ValueError(f'velocity должен быть числом, а не {type(velocity).__name__}')
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
    def cast_to_object_list(cls, country_aeroplanes: list[list]):
        aeroplane_list = []
        for aeroplane in country_aeroplanes:
            callsign = aeroplane[1].strip() # удаляем пробелы(с сервиса всегда идет 8 символов, добивают пробелами)
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