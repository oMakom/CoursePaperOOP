from src.aircraft_data_handler import Aeroplane
from src.api_connector import ApiAeroplanesCounty, ApiCountyCoordinates
from src.interface import (
    get_aeroplanes_by_country,
    filter_aeroplanes,
    get_aeroplanes_by_altitude,
    sort_aeroplanes,
    get_top_aeroplanes,
    print_all_aeroplanes,
)
from src.json_saver import JSONSaver

# Создание экземпляра класса для работы с API страны
api_county = ApiCountyCoordinates()
# Получение информации о коордмнатых страны с nominatim.openstreetmap.org
geo_coord = api_county.get_coordinates("RUSSIA")
# Создание экземпляра класса для работы с API самолетов
api_aeroplanes = ApiAeroplanesCounty()
# Получение информации о самолетах с opensky-network.org
aeroplanes_list = api_aeroplanes.get_aeroplanes(geo_coord)
# Преобразование набора данных в список объектов
aeroplanes = Aeroplane.cast_to_object_list(aeroplanes_list)
# Пример работы контструктора класса с одним самолетом
aeroplane = Aeroplane("UAL1621", "United States", 268.79, 10203.18)
aeroplane_2 = Aeroplane("UAL1621", "United States", 200.79, 10203.18)
aeroplane_3 = Aeroplane("UAL", "United States", 150.79, 10203.18)
print(aeroplane)
print(f"{aeroplanes[0].velocity}, {aeroplanes[0].altitude}")
print(f"{aeroplanes[2].velocity}, {aeroplanes[2].altitude}")
print(f"1 > 3 :{aeroplanes[0] > aeroplanes[2]}")
print(f"1 = 3 :{aeroplanes[0] == aeroplanes[2]}")
print(f"1 < 3 :{aeroplanes[0] < aeroplanes[2]}")
# Сохранение информации в файл
json_saver = JSONSaver()
json_saver.add_aeroplane(aeroplanes)
json_saver.add_aeroplane(aeroplane)
json_saver.add_aeroplane(aeroplane_2)
json_saver.add_aeroplane(aeroplane_3)
json_saver.delete_aeroplane("DMFEY")

# Функция для взаимодействия с пользователем


def user_interaction():
    country = input("Введите название страны: ").upper()  # Например RUSSIA
    aeroplanes = get_aeroplanes_by_country(country)

    # фильтрация по стране регистрации
    filter_words = (
        input("Введите названия стран для фильтрации по стране регистрации через запятую: ").title().split(",")
    )  # например United States, Germany
    filtered_aeroplanes = filter_aeroplanes(aeroplanes, filter_words)

    # фильтрация по диапазону высот полета
    altitude_range = input("Введите диапазон высот полета: ")  # Пример: 200 - 1000
    ranged_aeroplanes = get_aeroplanes_by_altitude(filtered_aeroplanes, altitude_range)

    # сортировка по высоте полета по убыванию
    sorted_by_altitude = sort_aeroplanes(ranged_aeroplanes)

    # вывод топ n самолетов
    top_n = int(input("Введите количество самолетов для вывода в топ N: "))
    top_n_aeroplanes = get_top_aeroplanes(sorted_by_altitude, top_n)

    # вывод результата
    print_all_aeroplanes(top_n_aeroplanes)


if __name__ == "__main__":
    user_interaction()
