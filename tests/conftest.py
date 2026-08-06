import os
import tempfile

import pytest

from src.aircraft_data_handler import Aeroplane


@pytest.fixture
def raw_open_sky_row():
    # Полная строка из states API OpenSky
    return [
        "4b1812",  # 0: icao24
        "SWR438A ",  # 1: callsign (с пробелами)
        "Switzerland",  # 2: country
        1766166618,  # 3: time_position
        1766166618,  # 4: last_contact
        -0.0168,  # 5: longitude
        51.0888,  # 6: latitude
        4267.2,  # 7: baro_altitude
        False,  # 8: on_ground
        189.7,  # 9: velocity
        129.39,  # 10: true_track
        14.63,  # 11: vertical_rate
        None,  # 12: sensors
        4282.44,  # 13: geo_altitude
        "2061",  # 14: squawk
        False,  # 15: spi
        0,  # 16: position_source
    ]


@pytest.fixture
def plane_a():
    return Aeroplane(callsign="SWR438A", country="Switzerland", velocity=250.0, altitude=10000)


@pytest.fixture
def plane_b():
    return Aeroplane(callsign="LH123", country="Germany", velocity=270.0, altitude=11000)


@pytest.fixture
def tmp_json_path():
    with tempfile.NamedTemporaryFile(mode="w+", suffix=".json", delete=False) as f:
        path = f.name
    yield path
    # очистка после теста
    if os.path.exists(path):
        os.remove(path)
