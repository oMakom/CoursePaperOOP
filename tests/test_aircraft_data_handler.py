import pytest

from src.aircraft_data_handler import Aeroplane


@pytest.mark.parametrize(
    "callsign_input,expected",
    [
        (None, "No callsign"),
        ("", "No callsign"),
        ("  FLT123  ", "FLT123"),
        ("SWR438A", "SWR438A"),
    ],
)
def test_callsign_normalization(callsign_input, expected):
    """Проверка инициализаци callsign класса"""
    plane = Aeroplane(callsign=callsign_input)
    assert plane.callsign == expected


def test_callsign_non_str_raises():
    """Вызов ошибки при числовом значении callsign"""
    with pytest.raises(ValueError):
        Aeroplane(callsign=12321)


@pytest.mark.parametrize(
    "country_input,expected",
    [
        (None, "None country"),
        ("", "None country"),
        ("  France  ", "France"),
        ("Germany", "Germany"),
    ],
)
def test_country_normalization(country_input, expected):
    """Проверка инициализаци country класса"""
    plane = Aeroplane(country=country_input)
    assert plane.country == expected


def test_country_non_str_raises():
    """Вызов ошибки при числовом значении country"""
    with pytest.raises(ValueError):
        Aeroplane(country=12321)


@pytest.mark.parametrize(
    "velocity_input,expected_value",
    [
        (None, 0.0),
        (0, 0.0),
        (100, 100.0),
        (50.5, 50.5),
    ],
)
def test_velocity_valid_values(velocity_input, expected_value):
    """Проверка инициализаци velocity класса"""
    plane = Aeroplane(velocity=velocity_input)
    assert plane.velocity == expected_value


def test_velocity_negative_raises():
    """Вызов ошибки при отрицательном значении velocity"""
    with pytest.raises(ValueError):
        Aeroplane(velocity=-1)


def test_velocity_non_number_raises():
    """Вызов ошибки при нечисловом значении velocity"""
    with pytest.raises(ValueError):
        Aeroplane(velocity="fast")


@pytest.mark.parametrize(
    "altitude_input,expected_value",
    [
        (None, 0.0),
        (-100, 0.0),
        (-0.1, 0.0),
        (0, 0.0),
        (1000, 1000.0),
        (3500.5, 3500.5),
    ],
)
def test_altitude_normalization_and_validation(altitude_input, expected_value):
    """Проверка инициализаци altitude класса"""
    plane = Aeroplane(altitude=altitude_input)
    assert plane.altitude == expected_value


def test_altitude_non_number_raises():
    """Вызов ошибки при нечисловом значении altitude"""
    with pytest.raises(ValueError):
        Aeroplane(altitude="high")


@pytest.mark.parametrize(
    "p1_args,p2_args,expected,description",
    [
        # eq: одинаковые скорость и высота
        (
            {"velocity": 100, "altitude": 5000},
            {"velocity": 100, "altitude": 5000},
            True,
            "eq",
        ),
        # eq: разная скорость
        (
            {"velocity": 100, "altitude": 5000},
            {"velocity": 90, "altitude": 5000},
            False,
            "eq",
        ),
        # lt: по скорости
        (
            {"velocity": 90, "altitude": 5000},
            {"velocity": 100, "altitude": 4000},
            True,
            "lt",
        ),
        # lt: скорость равна, по высоте
        (
            {"velocity": 100, "altitude": 4000},
            {"velocity": 100, "altitude": 5000},
            True,
            "lt",
        ),
        # gt: по скорости
        (
            {"velocity": 110, "altitude": 3000},
            {"velocity": 100, "altitude": 6000},
            True,
            "gt",
        ),
    ],
)
def test_comparison_operators(p1_args, p2_args, expected, description):
    """тесты для корерктности методов сравнения"""
    p1 = Aeroplane(**p1_args)
    p2 = Aeroplane(**p2_args)

    if "eq" in description:
        assert (p1 == p2) is expected
    elif "lt" in description:
        assert (p1 < p2) is expected
    elif "gt" in description:
        assert (p1 > p2) is expected


def test_with_non_aeroplane():
    """Проверка корректности создания 'пустого' самолета"""
    p = Aeroplane()
    assert p.callsign == "No callsign"
    assert p.country == "None country"
    assert p.altitude == 0
    assert p.velocity == 0


def test_cast_from_raw_open_sky_row(raw_open_sky_row):
    """Проверка корректности создания самолета из данных  Opensky"""
    result = Aeroplane.cast_to_object_list([raw_open_sky_row])
    assert len(result) == 1
    assert result[0].callsign == "SWR438A"
    assert result[0].country == "Switzerland"
    assert result[0].velocity == pytest.approx(189.7)
    assert result[0].altitude == pytest.approx(4267.2)


def test_to_dict_matches_attributes():
    """Проверка корректности превода самолета в словарь"""
    plane = Aeroplane(
        callsign="FLT123",
        country="Germany",
        velocity=250.0,
        altitude=3000.0,
    )
    d = plane.to_dict()
    assert d == {
        "callsign": "FLT123",
        "country": "Germany",
        "velocity": 250.0,
        "altitude": 3000.0,
    }


def test_to_dict_with_normalized_values():
    """Проверка корректности преобразования данных похзывного и страны"""
    plane = Aeroplane(callsign="  FLT456  ", country="  France  ")
    d = plane.to_dict()
    assert d["callsign"] == "FLT456"
    assert d["country"] == "France"


def test_print_aeroplane():
    """Проверка корректности строкового представления самолета"""
    plane = Aeroplane(
        callsign="FLT123",
        country="Germany",
        velocity=250.0,
        altitude=3000.0,
    )

    assert (
        str(plane)
        == f"Aeroplane(callsign={plane.callsign!r}, country={plane.country!r},"
           f" velocity={plane.velocity}, altitude={plane.altitude})"
    )
