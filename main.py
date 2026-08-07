from src.aircraft_data_handler import Aeroplane
from src.api_connector import ApiAeroplanesCountry, ApiCountryCoordinates
from src.interface import (filter_aeroplanes, get_aeroplanes_by_altitude, get_aeroplanes_by_country,
                           get_top_aeroplanes, print_all_aeroplanes, sort_aeroplanes)
from src.json_saver import JSONSaver

# Создание экземпляра класса для работы с API страны
api_county = ApiCountryCoordinates()
# Получение информации о коордмнатых страны с nominatim.openstreetmap.org
geo_coord = api_county.fetch_data("RUSSIA")
# Создание экземпляра класса для работы с API самолетов
api_aeroplanes = ApiAeroplanesCountry()
# Получение информации о самолетах с opensky-network.org
aeroplanes_list = api_aeroplanes.fetch_data(geo_coord)
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
    while True:
        country = input("Введите название страны (пример ввода: RUSSIA): ")  # Например RUSSIA
        if country:
            break
        print("Страна не может быть пустой.")
    try:
        aeroplanes = get_aeroplanes_by_country(country)
    except Exception as e:
        print(f"Ошибка при запросе данных: {e}")
        return
    if not aeroplanes:
        print("Данные о самолетах не получены. Завершение программы")
        return

    # фильтрация по стране регистрации
    filter_words = (
        input(
            "Введите названия стран для фильтрации по стране регистрации через запятую "
            "(пример ввода: United States, Germany): "
        )
        .strip()
        .split(",")
    )

    filtered_aeroplanes = filter_aeroplanes(aeroplanes, filter_words)

    # фильтрация по диапазону высот полета
    while True:
        altitude_range = input("Введите диапазон высот полета (Пример ввода: 200 - 10200): ")
        if altitude_range:
            range_list = altitude_range.split("-")
            try:
                altitude_min = int(range_list[0])
                altitude_max = int(range_list[1])

                if altitude_min >= altitude_max:
                    print("Минимальная высота должна быть меньше максимальной")
                if altitude_min < altitude_max:
                    ranged_aeroplanes = get_aeroplanes_by_altitude(filtered_aeroplanes, altitude_range)
                    break

            except ValueError:
                print("Высота должна быть числом")
        else:
            print("Данные диапазона высот не введены. Фильтрация по диапазону высот пропущена")
            ranged_aeroplanes = filtered_aeroplanes
            break

    # сортировка по высоте полета по убыванию
    sorted_by_altitude = sort_aeroplanes(ranged_aeroplanes)

    # вывод топ n самолетов
    while True:
        top_n = input("Введите количество самолетов для вывода в топ N: ").strip()
        try:
            n = int(top_n)
            if n > 0:
                break
            print("Число должно быть больше 0.")
        except ValueError:
            print("Введите целое число.")

    top_n_aeroplanes = get_top_aeroplanes(sorted_by_altitude, top_n)

    # вывод результата
    print_all_aeroplanes(top_n_aeroplanes)


if __name__ == "__main__":
    user_interaction()
