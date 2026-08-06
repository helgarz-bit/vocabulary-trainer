from utils import clear_screen, pause
import dictionary
import statistic
import trainer

MAIN_MENU_NAME = "ГЛАВНОЕ МЕНЮ"
DICTIONARY_MENU_NAME = "УПРАВЛЕНИЕ СЛОВАРЕМ"
FIND_MENU_NAME = "ПОИСК"
STATS_MENU_NAME = "СТАТИСТИКА"

MAIN_MENU = (
    ("1", "Управление словарем"),
    ("2", "Поиск"),
    ("3", "Тренировка"),
    ("4", "Статистика"),
("0", "Выход")
)

DICTIONARY_MENU = (
    ("1", "Добавить"),
    ("2", "Редактировать"),
    ("3", "Удалить"),
    ("0", "Назад")
)

FIND_MENU = (
    ("1", "Найти слово"),
    ("2", "Показать список всех слов"),
("0"    , "Назад")
)

STATS_MENU = (
    ("1", "Общая статистика"),
    ("2", "Статистика по словам"),
    ("3", "Трудные слова"),
    ("4", "Обнулить статистику"),
    ("0", "Назад")
)

#функция вывода меню на экран
def show_menu(menu_name: str, menu: tuple) -> str:
    clear_screen()
    print(menu_name)
    for key, item in menu:
        print(f"{key}. {item}")
    while True:
        choice = input("Выберите пункт меню")
        if choice in [key for key, item in menu]:        
            return choice
        print("Выбран некорректный вариант.")

    
def menu():
    while True:
        choice = show_menu(MAIN_MENU_NAME, MAIN_MENU)
    
        match choice:
            case "1": #управление словарем
                while True:
                    choice = show_menu(DICTIONARY_MENU_NAME,DICTIONARY_MENU)
                    match choice:
                        case "1":
                            dictionary.manager_dict("add")
                        case "2":
                            dictionary.manager_dict("edit")
                        case "3":
                            dictionary.manager_dict("delete")
                        case "0":
                            break
    
            case "2": #поиск
                while True:
                    choice = show_menu(FIND_MENU_NAME, FIND_MENU)
                    match choice:
                        case "1":
                            dictionary.manager_dict("find")
                        case "2":
                            dictionary.manager_dict("all")
                        case "0":
                            break
                         
            case "3": #тренировка
                trainer.start_session()

            case "4": #статистика
                while True:
                    choice = show_menu(STATS_MENU_NAME, STATS_MENU)
                    match choice:
                        case "1":
                            statistic.manager_stats("total")
                        case "2":
                                  statistic.manager_stats("stats_word")
                        case "3":
                            statistic.manager_stats("dificault")
                        case "4":
                            statistic.manager_stats("rewrite")
                        case "0":
                            break

            case "0": #выход
                break
    