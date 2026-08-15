import json
import os.path
from datetime import date

from config import FIELDS_FOR_SAVE

vocabulary = {}
stats = {}
categories = []

#функция загрузки из файла
def load_json(file_name: str, default: dict|list) -> dict|list:
    if not os.path.exists(file_name):
           return default
    with open(file_name, "r", encoding="utf-8") as file:
        data = json.load(file)

    return data

#функция выгрузки данных в файл
def save_json(data: dict|list, file_name: str) -> None:
    with open(file_name, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

def load(dict_name: dict, file_name: str) ->None:
    dict_name.clear()
    dict_name.update(load_json(file_name, {}))

    #перевод даты в словаре из строки в объект date
def convert_string_to_date(dictionary: dict, field_name: str) -> None:
    for value in dictionary.values():
            if value[field_name] != None:
              value[field_name] = date.fromisoformat(value[field_name])
            else:
                value[field_name] = None

                #преобразование даты из объекта в строку
def convert_date_to_string(dictionary: dict, field_name: str) -> None:
     for value in dictionary.values():
          if value[field_name] is not None:
               value[field_name] =value[field_name].isoformat() 

#удаление ненужных полей из словаря перед сохранением в файл
def prepare_dict_for_save(dictionary: dict) -> dict:
    dict_for_save = {
     word: {
          field: data[field]
          for field  in FIELDS_FOR_SAVE
     }
     for word, data in dictionary.items()
}

    return dict_for_save