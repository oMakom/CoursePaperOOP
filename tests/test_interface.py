from unittest.mock import patch

from src.api_connector import ApiCountryCoordinates
from src.interface import filter_aeroplanes, get_aeroplanes_by_altitude, sort_aeroplanes, get_top_aeroplanes, \
    print_all_aeroplanes, get_aeroplanes_by_country


def test_filter_aeroplanes():
    data = [
        {"callsign": "A1", "country": "France", "velocity": 100, "altitude": 5000},
        {"callsign": "B1", "country": "United States", "velocity": 200, "altitude": 6000},
        {"callsign": "C1", "country": "Poland", "velocity": 300, "altitude": 7000},
    ]
    filtered = filter_aeroplanes(data, ["france", "UNITED States"])
    assert len(filtered) == 2
    assert filtered[0]["country"] == "France"
    assert filtered[1]["country"] == "United States"


def test_filter_aeroplanes_empty_filter():
    data = [{"callsign": "A1", "country": "France", "velocity": 100, "altitude": 5000}]
    filtered = filter_aeroplanes(data, [])
    assert len(filtered) == 1


def test_sort_and_top():
    data = [
        {"callsign": "A", "country": "X", "velocity": 10, "altitude": 100},
        {"callsign": "B", "country": "Y", "velocity": 20, "altitude": 300},
        {"callsign": "C", "country": "Z", "velocity": 30, "altitude": 200},
    ]
    sorted_data = sort_aeroplanes(data)
    assert sorted_data[0]["altitude"] == 300
    assert sorted_data[1]["altitude"] == 200
    assert sorted_data[2]["altitude"] == 100

    top_2 = get_top_aeroplanes(sorted_data, 2)
    assert len(top_2) == 2
    assert top_2[0]["altitude"] == 300
    assert top_2[1]["altitude"] == 200

@patch.object(ApiCountryCoordinates, "fetch_data", return_value=[])
def test_get_aeroplanes_by_country_no_coords(mock_api_coords):
    result = get_aeroplanes_by_country("UnknownCountry")
    assert result == []

def test_print_all_aeroplanes(capsys):
    data = [
        {"callsign": "A1", "country": "France", "velocity": 100, "altitude": 5000},
    ]
    print_all_aeroplanes(data)
    captured = capsys.readouterr()
    assert "A1" in captured.out
    assert "France" in captured.out
