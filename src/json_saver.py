import json
import os
from abc import ABC, abstractmethod

from src.aircraft_data_handler import Aeroplane

root_path = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.abspath(os.path.join(root_path, "..", "data/data_aeroplanes.json"))


class BaseSaver(ABC):
    @abstractmethod
    def add_aeroplane(self, aeroplane: "list[Aeroplane] | Aeroplane") -> None:
        pass

    @abstractmethod
    def delete_aeroplane(self, criteria: str) -> None:
        pass


class JSONSaver(BaseSaver):
    """класс для добавления и удаления информации о самолетах в/из JSON-файл"""

    def __init__(self):
        self.__data_path = data_path

    @staticmethod
    def obj_to_list(aeroplane_obj: "list[Aeroplane] | Aeroplane") -> list[dict]:
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

    def reaf_data_file(self):
        """Читает данные из файла "../data/data_aeroplanes.json", если ошибка чтения, то на выходе пустой список"""
        try:
            with open(self.__data_path, "r", encoding="utf-8") as f:
                data_f = json.load(f)
                if not isinstance(data_f, list):
                    data_f = []
        except (json.JSONDecodeError, IOError):
            data_f = []
        return data_f

    def write_to_json(self, data_list: list):
        """Записывает данные в файл "../data/data_aeroplanes.json" """
        with open(self.__data_path, "w", encoding="utf-8") as f:
            json.dump(data_list, f, ensure_ascii=False, indent=4)

    def add_aeroplane(self, aeroplane: "list[Aeroplane] | Aeroplane"):
        """класс для сохранения информации о самолетах в JSON-файл"""
        # Чтение переданных данных
        data = JSONSaver.obj_to_list(aeroplane)
        # Работа с файлом
        key = set()  # хранит позывные самолетов
        if os.path.isfile(self.__data_path):
            # Получаем данные из файла
            data_file = JSONSaver.reaf_data_file(self)
            # собираем все ключи из файла(принимаем, что дублей в файле нету)
            for item_file in data_file:
                key.add(item_file["callsign"])
            # сверяем уникальные ключи записанных данных
            for item in data:
                if item.get("callsign") is not None and item.get("callsign") not in key:
                    key.add(item["callsign"])
                    data_file.append(item)
            # Перезаписываем файл без дублей
            JSONSaver.write_to_json(self, data_file)
        else:
            # Файла нет - создаем новый
            date_new = []
            # собираем все ключи
            for item_file in data:
                key.add(item_file["callsign"])
            for item in data:
                if item.get("callsign") is not None and item.get("callsign") not in key:
                    key.add(item["callsign"])
                    date_new.append(item)
            # Перезаписываем файл без дублей
            JSONSaver.write_to_json(self, date_new)

    def delete_aeroplane(self, criteria: str):
        """удвляет данные из файла по позывному"""
        # Получаем данные из файла
        data_file = JSONSaver.reaf_data_file(self)
        date_new = []
        for item in data_file:
            if item.get("callsign") != criteria:
                date_new.append(item)
        JSONSaver.write_to_json(self, date_new)
