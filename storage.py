import json
import os.path

vocabulary = {}
stats = {}

#функция загрузки из файла
def load_json(file_name: str) -> dict:
    if not os.path.exists(file_name):
           return {}               
    with open(file_name, "r", encoding="utf-8") as file:
        data = json.load(file)

    return data

#функция выгрузки словаря в файл
def save_json(data: dict, file_name: str) -> None:
    with open(file_name, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

def load(dict_name: dict, file_name: str) ->None:
    dict_name.clear()
    dict_name.update(load_json(file_name))