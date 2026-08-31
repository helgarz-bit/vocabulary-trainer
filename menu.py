from utils import clear_screen
from dictionary import manager_dict, manager_categories
from statistic import manager_stats
from trainer import start_session

NAME = "name"
TITLE = "title"
OBJECT = "object"
ITEMS = "items"
ARGUMENT = "argument"


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
             "object": manager_categories,},
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
        "3": {
             "title": "Поиск по категории",
             "object": manager_dict,
             "argument": "find_by_cat"
        },
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
              "title": "Сводная таблица прогресса изучения слов",
              "object": manager_stats,
              "argument": "summary"
         },
    "5": {
         "title": "Обнулить статистику",
         "object": manager_stats,
         "argument": "reset"},
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
    """Отображает меню и запрашивает у пользователя выбор пункта меню.
    
    Очищает экран, выводит название меню и список доступных пунктов.
    Затем запрашивает у пользователя пункт меню, пока не будет введен корректный вариант
    
    Args:
        menu: Словарь с данными меню, должен содержать название меню
        и словарь с пунктами меню.
        
    Returns:
        Ключ выбранного пользователем пункта меню в виде строки.
        """
    clear_screen()
    print(menu[NAME])
    items= menu[ITEMS]
    for key, item in items.items():
        print(f"{key}. {item[TITLE]}")
    while True:
        choice = input("Выберите пункт меню")
        if choice in items:
            return choice
        print("Выбран некорректный вариант.")

#раскрывает вложенное меню или запускает функцию
def process_menu(menu: dict) -> None:
    """Обрабатывает выбранные пользователем пункты меню.
    
    Если выбран пункт вложенного меню, рекурсивно
    обрабатывает это меню.  Если выбран 
    вызываемый объект, вызывает объект с аргументом,
    если аргумент указан в данных пункта меню.
    
    Args:
        menu: Словарь с данными меню. Каждый пункт должен содержать
объект для обработки: вложенное меню или вызываемую функцию. 
Для вызываемой функции может быть указан аргумент.
    """
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
    