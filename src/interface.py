import pandas as pd

from src.aircraft_data_handler import Aeroplane
from src.api_connector import ApiAeroplanesCountry, ApiCountryCoordinates
from src.json_saver import JSONSaver


def get_aeroplanes_by_country(country: str):
    """Получает данные по API по кориднатам страны"""
    api_county = ApiCountryCoordinates()
    geo_coord = api_county.fetch_data(country.upper())
    if geo_coord == []:
        return geo_coord
    api_aeroplanes = ApiAeroplanesCountry()
    aeroplanes_list = api_aeroplanes.fetch_data(geo_coord)
    aeroplanes_obj = Aeroplane.cast_to_object_list(aeroplanes_list)
    aeroplanes = JSONSaver.obj_to_list(aeroplanes_obj)
    return aeroplanes


# фильтрация по стране регистрации
def filter_aeroplanes(aeroplanes: list[dict], filter_words: list[str]) -> list[dict]:
    """Оставляет список самолетов только по указанным странам регистрации"""
    if filter_words == [""] or (not filter_words):
        print("Данные стрны/стран для фильтрации не введены. Фильтрация по стране пропущена")
        filtered_aeroplanes = aeroplanes
        return filtered_aeroplanes
    df = pd.DataFrame(aeroplanes)
    filter_words_no_space = [country.title().strip() for country in filter_words]
    df_sort_country_reg = df.loc[df.country.isin(filter_words_no_space)]
    df_dict = df_sort_country_reg.to_dict(orient="records")
    return df_dict


# фильтрация по диапазону высот полета
def get_aeroplanes_by_altitude(aeroplanes: list[dict], altitude_range) -> list[dict]:
    """Выбирает из списка самолеты в пределах указанной высоты"""
    df = pd.DataFrame(aeroplanes)
    range_list = altitude_range.split("-")
    aeroplanes_by_altitude = df.loc[(df.altitude >= float(range_list[0])) & (df.altitude <= float(range_list[1]))]
    df_dict = aeroplanes_by_altitude.to_dict(orient="records")
    return df_dict


# сортировка по высоте самолетов (от большего к меньшему)
def sort_aeroplanes(aeroplanes: list[dict]) -> list[dict]:
    """Сортирует самолеты по высоте по убыванию"""
    df = pd.DataFrame(aeroplanes)
    sort_by_altitude = df.sort_values(by="altitude", ascending=False)
    df_dict = sort_by_altitude.to_dict(orient="records")
    return df_dict


# получение топ N самолетов
def get_top_aeroplanes(aeroplanes: list[dict], top_n: int) -> list[dict]:
    """Оставляет только перые top_n самолетов из списка"""
    result = []
    number = 0
    for aeroplane in aeroplanes:
        if number >= int(top_n):
            break
        result.append(aeroplane)
        number += 1
    return result


def print_all_aeroplanes(aeroplanes: list[dict]) -> None:
    """Фнукция для печати каждого самолета на отельно строке"""
    for aeroplane in aeroplanes:
        print(aeroplane)
