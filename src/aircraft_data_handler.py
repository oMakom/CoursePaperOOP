from unittest import result


class Aeroplane:
    def __init__(self, callsign = None,country = None, velocity = None,altitude =None ):
        self.callsign = callsign
        self.country = country
        self.velocity = velocity
        self.altitude = altitude

    @classmethod
    def cast_to_object_list(cls, country_aeroplanes: list[list]):
        aeroplane_list = []
        for aeroplane in country_aeroplanes:
            callsign = aeroplane[1]
            country = aeroplane[2]
            velocity = aeroplane[9]
            altitude = aeroplane[7]
            single_aeroplane = Aeroplane(callsign, country, velocity, altitude)
            aeroplane_list.append(single_aeroplane)
        return aeroplane_list

    def __eq__(self, other):
        """Равенство объектов (сравнение самолетов между собой по скорости и высоте)"""
        if self.velocity == other.velocity and self.altitude == other.altitude:
            return True
        return False

    def __gt__(self, other):
        """Больше (сравнение самолетов между собой по скорости и высоте)"""
        if self.velocity > other.velocity:
            return True
        if self.altitude > other.altitude:
            return True
        return False

    def __lt__(self, other):
        """Меньше (сравнение самолетов между собой по скорости и высоте)"""
        if self.velocity < other.velocity:
            return True
        if self.altitude < other.altitude:
            return True
        return False