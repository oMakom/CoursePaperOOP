from unittest import result


class Aeroplane:
    def __init__(self, callsign = None,country = None, velocity = None,altitude =None ):
        self.callsign = callsign
        self.country = country
        self.velocity = velocity
        self.altitude = altitude

    @classmethod
    def cast_to_object_list(cls, country_aeroplanes: list[list]):
        aeroplane_dict = []
        for aeroplane in country_aeroplanes:
            callsign = aeroplane[1]
            country = aeroplane[2]
            velocity = aeroplane[9]
            altitude = aeroplane[7]
            single_aeroplane = Aeroplane(callsign, country, velocity, altitude)
            aeroplane_dict.append(single_aeroplane)
        return aeroplane_dict
