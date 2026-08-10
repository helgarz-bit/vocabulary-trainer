from utils import clear_screen
from dictionary import manager_dict
from statistic import manager_stats
from trainer import start_session

NAME = "name"
TITLE = "title"
OBJECT = "object"
ITEMS = "items"
ARGUMENT = "argument"

CATEGORY_MENU = {
     "name": "УПРАВЛЕНИЕ КАТЕГОРИЯМИ",
     "items": {
          "1": {
               "title": "Добавление категории",
               "object": manager_dict,
               "argument": "add_cat"},
               "2": {
                    "title": "Редактирование категории",
                    "object": manager_dict,
                    "argument": "edit_cat",},
                    "3": {
                         "title": "Удаление категории",
                         "object": manager_dict,
                         "argument": "delete_cat"},
                         "0": {
                              "title": "Назад"}
     }}

DICTIONARY_MENU = {
    "name": "УПРАВЛЕНИЕ СЛОВАРЕМ",
    "items": {
    "1": {
        "title": "Добавить слово", 
        "object": manager_dict, 
"argument":         "add"},
    "2": {
        "title": "Редактировать слово",
        "object": manager_dict,
        "argument": "edit"},
    "3": {
        "title": "Удалить слово",
        "object": manager_dict,
        "argument": "delete"},
        "4": {
             "title": "Управление категориями",
             "object": CATEGORY_MENU,},
    "0": {
        "title": "Назад"}
}
}
FIND_MENU = {
     "name": "ПОИСК",
    "items": {
         "1": {
         "title": "Найти слово",
         "object": manager_dict,
         "argument": "find"},
    "2": {
        "title": "Показать список всех слов",
        "object": manager_dict,
        "argument": "all"},
"0": {
    "title": "Назад"}
    }}

STATS_MENU = {
     "name": "СТАТИСТИКА",
     "items": {
    "1": {
         "title": "Общая статистика",
         "object": manager_stats,
         "argument": "total"},
    "2": {
         "title": "Статистика по словам",
         "object":  manager_stats,
         "argument": "stats_word"},
    "3": {
         "title": "Трудные слова",
         "object": manager_stats,
         "argument": "difficult"},
    "4": {
         "title": "Обнулить статистику",
         "object": manager_stats,
         "argument": "default"},
    "0": {
         "title": "Назад"}
}}

MAIN_MENU = {
    "name": "ГЛАВНОЕ МЕНЮ",
    "items": {
    "1": {
    "title": "Управление словарем", 
    "object": DICTIONARY_MENU},
    "2": {
    "title": "Поиск", 
    "object": FIND_MENU},
    "3": {
        "title": "Тренировка", 
        "object": start_session},
    "4": {
        "title": "Статистика", 
        "object": STATS_MENU},
"0":  {
"title": "Выход"}
}}


#функция вывода меню на экран
def show_menu(menu: dict) -> str:
    clear_screen()
    print(menu[NAME])
    items= menu[ITEMS]
    for key, item in items.items():
        print(f"{key}. {item[TITLE]}")
    while True:
        choice = input("Выберите пункт меню")
        if choice in [key for key in items.keys()]:
            return choice
        print("Выбран некорректный вариант.")

#раскрывает вложенное меню или запускает функцию
def process_menu(menu: dict) -> None:
    while True:
        choice =     show_menu(menu)
        if choice == "0":
                    return
                
        object_name = menu[ITEMS][choice][OBJECT]

        if isinstance(object_name, dict):
            process_menu(object_name)
        elif callable(object_name):
            arg = menu[ITEMS][choice].get(ARGUMENT)
            if arg is not None:
                object_name(arg)
            else:
                object_name()
    
def menu() -> None:
    process_menu(MAIN_MENU)
    return