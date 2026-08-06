import json

from src.json_saver import JSONSaver


def test_single_object(plane_a):
    data = JSONSaver.obj_to_list(plane_a)
    assert len(data) == 1
    assert data[0]["callsign"] == "SWR438A"
    assert data[0]["country"] == "Switzerland"


def test_list_of_objects(plane_a, plane_b):
    data = JSONSaver.obj_to_list([plane_a, plane_b])
    assert len(data) == 2
    callsigns = {d["callsign"] for d in data}
    assert "SWR438A" in callsigns
    assert "LH123" in callsigns


def test_add_multiple_planes(tmp_path, plane_a, plane_b):
    test_file = tmp_path / "data_aeroplanes.json"

    saver = JSONSaver(file_path=str(test_file))
    saver.add_aeroplane([plane_a, plane_b])

    with open(test_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    assert len(data) == 2
    callsigns = {d["callsign"] for d in data}
    assert "SWR438A" in callsigns
    assert "LH123" in callsigns


def test_add_single_plane(tmp_path, plane_a):
    test_file = tmp_path / "data_aeroplanes.json"
    saver = JSONSaver(file_path=str(test_file))
    saver.add_aeroplane(plane_a)

    with open(test_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    assert len(data) == 1
    assert data[0]["callsign"] == "SWR438A"


def test_no_duplicates_by_callsign(tmp_path, plane_a):
    """Повторное добавление самолёта с тем же позывным не должно создавать дубль."""
    test_file = tmp_path / "data.json"
    saver = JSONSaver(file_path=str(test_file))

    saver.add_aeroplane(plane_a)
    saver.add_aeroplane(plane_a)  # Повтор

    with open(test_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    assert len(data) == 1  # Дубль не добавлен
    assert data[0]["callsign"] == "SWR438A"


def test_delete_aeroplane(tmp_path, plane_a, plane_b):
    """Удаление самолёта по позывному."""
    test_file = tmp_path / "data.json"
    saver = JSONSaver(file_path=str(test_file))

    saver.add_aeroplane([plane_a, plane_b])
    saver.delete_aeroplane("SWR438A")

    with open(test_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    callsigns = {d["callsign"] for d in data}
    assert "SWR438A" not in callsigns
    assert "LH123" in callsigns
    assert len(data) == 1


def test_delete_non_existing_callsign_does_nothing(tmp_path, plane_a):
    """Удаление несуществующего позывного"""
    test_file = tmp_path / "data.json"
    saver = JSONSaver(file_path=str(test_file))

    saver.add_aeroplane(plane_a)
    saver.delete_aeroplane("NONEXIST")

    with open(test_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    assert len(data) == 1
    assert data[0]["callsign"] == "SWR438A"


def test_read_corrupted_json_returns_empty_list(tmp_path):
    """Если файл есть, но JSON битый — read_data_file должен вернуть пустой список."""
    test_file = tmp_path / "data.json"

    # Создаём битый JSON вручную
    with open(test_file, "w", encoding="utf-8") as f:
        f.write("{ invalid json }")

    saver = JSONSaver(file_path=str(test_file))
    data = saver.read_data_file()

    assert isinstance(data, list)
    assert len(data) == 0


def test_write_to_json_creates_file_if_not_exists(tmp_path):
    """write_to_json должен создавать файл, если его нет."""
    test_file = tmp_path / "new_data.json"
    assert not test_file.exists()

    saver = JSONSaver(file_path=str(test_file))
    saver.write_to_json([{"callsign": "TEST"}])

    assert test_file.exists()
    with open(test_file, "r", encoding="utf-8") as f:
        data = json.load(f)
    assert len(data) == 1
    assert data[0]["callsign"] == "TEST"


def test_obj_to_list_handles_single_and_list(plane_a, plane_b):
    """Проверка статического метода obj_to_list."""
    # Одиночный объект
    result_single = JSONSaver.obj_to_list(plane_a)
    assert isinstance(result_single, list)
    assert len(result_single) == 1
    assert result_single[0]["callsign"] == "SWR438A"

    # Список объектов
    result_list = JSONSaver.obj_to_list([plane_a, plane_b])
    assert isinstance(result_list, list)
    assert len(result_list) == 2
    assert result_list[0]["callsign"] == "SWR438A"
    assert result_list[1]["callsign"] == "LH123"
