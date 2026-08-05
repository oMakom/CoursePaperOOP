from unittest.mock import patch

from src.api_connector import ApiAeroplanesCountry, ApiCountryCoordinates


@patch("src.api_connector.get")
def test_api_country_coordinates_success(mock_get):
    """Проверка корректного получении координат по стране"""
    mock_response = mock_get.return_value
    mock_response.ok = True
    mock_response.raise_for_status.return_value = None
    mock_response.json.return_value = [{"boundingbox": ["55.75", "55.80", "37.60", "37.70"]}]

    client = ApiCountryCoordinates()
    result = client.fetch_data("Russia")

    assert result == ["55.75", "55.80", "37.60", "37.70"]


@patch("src.api_connector.get")
def test_api_country_coordinates_not_found(mock_get):
    """Проверка корректного получении координат по ненайденной стране"""
    mock_response = mock_get.return_value
    mock_response.ok = True
    mock_response.raise_for_status.return_value = None
    mock_response.json.return_value = []

    client = ApiCountryCoordinates()
    result = client.fetch_data("НеизвестнаяСтрана")

    assert result == []


@patch("src.api_connector.get")
def test_api_aeroplanes_county_success(mock_get):
    """Проверка корректного получения самолетов"""
    mock_response = mock_get.return_value
    mock_response.ok = True
    mock_response.raise_for_status.return_value = None
    mock_response.json.return_value = {
        "states": [
            ["4b1812", "SWR438A", "Switzerland", None, None, 8.5, 47.0, 10000, None, 250],
            ["abcd12", "TEST123", "Germany", None, None, 9.0, 48.0, 11000, None, 300],
        ]
    }

    client = ApiAeroplanesCountry()
    result = client.fetch_data(["8.0", "10.0", "46.0", "50.0"])

    assert isinstance(result, list)
    assert len(result) == 2
    assert result[0][0] == "4b1812"
    assert result[1][1] == "TEST123"


@patch("src.api_connector.get")
def test_api_aeroplanes_county_invalid_coords_length(mock_get):
    """Проверка получения некорректных координат (3 вместо 4х)"""
    client = ApiAeroplanesCountry()
    result = client.fetch_data(["8.0", "10.0", "46.0"])

    assert result is None
    mock_get.assert_not_called()


@patch("src.api_connector.get")
def test_api_aeroplanes_county_network_error(mock_get):
    """Проверка ошибки запроса по превышению времени ожидания"""
    from requests.exceptions import RequestException

    mock_get.side_effect = RequestException("Timeout")

    client = ApiAeroplanesCountry()
    result = client.fetch_data(["8.0", "10.0", "46.0", "50.0"])

    assert result is None
