import json
import os
from abc import ABC, abstractmethod

from src.aircraft_data_handler import Aeroplane

root_path = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.abspath(os.path.join(root_path, "..", "data/data_aeroplanes.json"))


class BaseSaver(ABC):
    @abstractmethod
    def add_aeroplane(self, aeroplane: list[Aeroplane] | Aeroplane) -> None:
        pass

    @abstractmethod
    def delete_aeroplane(self, criteria: str) -> None:
        pass


class JSONSaver(BaseSaver):
    """класс для добавления и удаления информации о самолетах в/из JSON-файл"""

    def __init__(self, file_path=None):
        if file_path is None:
            # Если путь не передан — берём из глобальной переменной
            self.__data_path = data_path
        else:
            # Для тестов передаём свой путь явно
            self.__data_path = os.path.abspath(file_path)

    @staticmethod
    def obj_to_list(aeroplane_obj: list[Aeroplane] | Aeroplane) -> list[dict]:
        """Принимает объект, либо список объектов. Приводит в виду list[dict]"""
        data = []
        if not isinstance(aeroplane_obj, list):
            data = [
                {
                    "callsign": aeroplane_obj.callsign,
                    "country": aeroplane_obj.country,
                    "velocity": aeroplane_obj.velocity,
                    "altitude": aeroplane_obj.altitude,
                }
            ]
        if isinstance(aeroplane_obj, list):
            for one_aeroplane in aeroplane_obj:
                data_aeroplane = {
                    "callsign": one_aeroplane.callsign,
                    "country": one_aeroplane.country,
                    "velocity": one_aeroplane.velocity,
                    "altitude": one_aeroplane.altitude,
                }
                data.append(data_aeroplane)
        return data

    def read_data_file(self) -> list[dict]:
        """Читает данные из файла "../data/data_aeroplanes.json", если ошибка чтения, то на выходе пустой список"""
        try:
            with open(self.__data_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                if not isinstance(data, list):
                    return []
                return data
        except (json.JSONDecodeError, IOError, FileNotFoundError):
            return []

    def write_to_json(self, data_list: list) -> None:
        """Записывает данные в файл "../data/data_aeroplanes.json" """
        with open(self.__data_path, "w", encoding="utf-8") as f:
            json.dump(data_list, f, ensure_ascii=False, indent=4)

    def add_aeroplane(self, aeroplane: list[Aeroplane] | Aeroplane) -> None:
        """метод для сохранения/добавления информации о самолетах в JSON-файл"""
        # Чтение переданных данных
        data = self.obj_to_list(aeroplane)
        # Работа с файлом
        key = set()  # хранит позывные самолетов
        if os.path.isfile(self.__data_path):
            # Получаем данные из файла
            data_file = self.read_data_file()
            # собираем все ключи из файла(принимаем, что дублей в файле нету)
            for item_file in data_file:
                key.add(item_file["callsign"])
            # сверяем уникальные ключи записанных данных
            for item in data:
                if item.get("callsign") is not None and item.get("callsign") not in key:
                    key.add(item["callsign"])
                    data_file.append(item)
            # Перезаписываем файл без дублей
            self.write_to_json(data_file)
        else:
            # Файла нет - создаем новый c проверкой дублей
            data_new = []
            for item in data:
                if item.get("callsign") is not None and item.get("callsign") not in key:
                    key.add(item["callsign"])
                    data_new.append(item)
            # Перезаписываем файл без дублей
            self.write_to_json(data_new)

    def delete_aeroplane(self, callsign: str) -> None:
        """удаляет данные из файла по позывному"""
        # Получаем данные из файла
        data_file = self.read_data_file()
        if data_file is None:
            return
        else:
            filtered_data = []
            for item in data_file:
                if item.get("callsign") != callsign:
                    filtered_data.append(item)
            self.write_to_json(filtered_data)
