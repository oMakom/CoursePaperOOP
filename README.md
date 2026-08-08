# Курсовая работа по ООП (4й модуль)
В этой работе реализована программа, которая собирает данные о самолетах в воздушных пространствах тех стран,
которые выберет пользователь.  
Чтобы получить географические координаты стран используется API `nominatim.openstreetmap.org`,
а чтобы получить информацию о самолетах — API `opensky-network.org`.
## Установка:

1. Клонируйте репозиторий:
```
https://github.com/oMakom/CoursePaperOOP.git
```

2. Установите зависимости:
```
pip install -r requirements.txt
poetry install
```

### Реализация класса для работы с информацией о самолетах`Aeroplane(callsign: str, country: str, velocity: float, altitude: float)`
- **Класс реализованы в модуле aircraft_data_handler.py**
- cast_to_object_list(cls, country_aeroplanes: list[dict]) - Создает из списка словарей список объектов Aeroplane
- __eq__ __gt__ __lt__ - методы сравнения по скорости и высоте
- __str__ - метод для вывода в читаемом виде
- to_dict - метод преобразования в словарь
### Реализация класса для работы с файлами`JSONSaver(self, file_path=None)`
- **Класс реализованы в модуле json_saver.py**
- obj_to_list(aeroplane_obj: list[Aeroplane] | Aeroplane) - Принимает объект, либо список объектов. Приводит в виду list[dict]
- read_data_file() - """Читает данные из файла "../data/data_aeroplanes.json", если ошибка чтения, то на выходе пустой список"""
- write_to_json(data_list: list) - Записывает данные в файл ( по умолчанию "../data/data_aeroplanes.json") 
- add_aeroplane(aeroplane: list[Aeroplane] | Aeroplane) - метод для сохранения/добавления информации о самолетах в JSON-файл
- delete_aeroplane(self, callsign: str) - метод удаляет данные из файла по позывному
### Реализация класса для работы Api ApiCountryCoordinates() и ApiAeroplanesCountry()`
- **Классы реализованы в модуле api_connector.py**
- fetch_data - метод получения данных из API

- ### Функционал интерфейса реализован в модуле interface.py
- ### Пробный вызов функционала и связующая интерфес функция вызваны в модуле main.py
