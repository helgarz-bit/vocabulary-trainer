import os

from config import ACTIONS, PROMPT

#функция диалога с ответами "да"\"нет"
def answer_dialog(prompt: str) -> bool:
    while True:
        answer = input(f"{prompt} Введите y/n(д/н): ").strip().lower()
            
        if answer in {'y', 'д'}:
            return True
        elif answer in {'n', 'н'}:
            return False
        print("Введен недопустимый вариант. Попробуйте еще раз!")

#управление действием
def what_to_do(repeat: bool, action: str|None =None) -> str:
    prompt = ""
    if repeat:
        prompt = f"r - повторить {ACTIONS[action][PROMPT]}."
    while True:
        do = input(f'm - вернуться в меню\n{prompt}')
        if do == "m":
            return "return"
        elif repeat and do == "r":
            return action
        else:
            print("Введена недопустимая команда. Попробуйте еще раз!")

#функция проверки ввода слова
def check_valid(value: str) -> bool:
    """Проверяет слово на соответствие правилам написания слова.
    
    Строка должна начинаться с буквы и заканчиваться ею.
    Внутри строки допускаются буквы. апострофы, дефисы и пробелы.
    Два символа, не являющихся буквами, не могут следовать друг за другом подряд.
    
    Args:
        value: Строка, которую необходимо проверить.
        
    Returns:
        True, если строка соответствует правилам,
        False - иначе.
    """
#проверка первого символа
    char = value[0]
    if not char.isalpha():
        print("Слово должно начинаться с буквы! ")
        return False

    prev_char = ""
    for char in value[1:]:
        if char.isalpha():
            prev_char = char
            continue
        elif char in {" ", "'", "-"}:
            if not prev_char.isalpha():
                return False
            prev_char = char
        else:
            return False
#проверка последнего символа
    if not char.isalpha():
        return False
    return True
    
#функция обработки ввода  слова
def input_dialog(prompt: str,settings: dict, old_value: str|None = None) -> str|None:
    """Запрашивает значение  строковой переменной 
    у пользователя и обрабатывает его.
    
    Пользователь может ввести q для отмены ввода.
    При редактировании пустой ввод оставляет прежнее значение.
    Для обязательного поля пустой ввод не допускается.
    В зависимости от настроек, введенное значение может быть приведено к нижнему регистру
    и проверено на соответствие правилам ввода.
    
    Args: 
        prompt: Текст приглашения для ввода.
         settings:  Настройки поля, должны содержатьпараметры
         required, to_lower, validation.
         old_value: Предыдущее значение поля при редактировании.
         Если указано, то пустой ввод возвращает это значение.
         
     Returns:
        Введенное и обработанное значение. Возвращает old_value при пустом
        вводе при редактировании или None, если пользователь отменил ввод.
    """ 
    while True:
        in_value = input(f'{prompt} ').strip()
        if in_value == 'q':
            return None

        if  not in_value: #строка пустая
            if old_value is not None: #редактирование нажата enter
                return old_value
            #введена пустая строка
            if settings["required"]: #поле является обязательным
                print("Значение не может быть пустым. Попробуйте еще раз!")
                continue

        #строка не пустая
        if settings["to_lower"]:
            in_value = in_value.lower()
        if settings["validation"]:
            if not check_valid(in_value):    
                print("Значение имеет недопустимый формат. Попробуйте еще раз!")
                continue
            
        return in_value

#проверка ввода числовых значений
def input_number(prompt: str, min_value: int, max_value: int, old_value: int|None) -> int|None:
    while True:
        number = input(prompt).strip()
        if number == 'q':
            return None
        elif not number: #строка пустая
            if old_value is not None:
                return old_value
            print("Значение не может быть пустым. Попробуйте еще раз!")
            continue
        #строка не пустая
        if not number.isnumeric():
            print("Введенное значение не является числом. Попробуйте еще раз!")
            continue
        #если число, проверяем диапазон
        number = int(number)
        if number < min_value or number > max_value:
            print("Введенное значение вне допустимого диапазона. Попробуйте еще раз!")
            continue

        return number

#выбор из списка значений
def choose_item(items: list, default_index: int|None =None, old_value: str|None =None, message: str|None=None) -> int|None:
    """Запрашивает у пользователя выбор элемента из списка.
    
    Пользователь может выбрать элемент, введя его порядковый номер,
    либо использовать специальные команды:
    q - отменяет выбор, a - возвращает значение -1.
    При пустом вводе возвращается предыдущее значение, если оно указано.
    Если предыдущего значения нет, используется значение по умолчанию, если указано.

    Args:
        items: Список элементов, из которого проводится выбор.
        default_index: Индекс элемента, используемого по умолчанию при пустом вводе.
        old_value: Предыдущее значение элемента. Используется  при редактировании
        для сохранения текущего выбора.
        message: Дополнительное сообщение.
         
    Returns: 
        Индекс выбранного элемента. -1 при выборе команды 'a'
        None при отмене выбора.
    """
    if message is not None:
        print(message)
    print("q - отмена")
    while True:
        choice  = input("Выберите вариант:  ").strip()

        if choice == 'q':
            if old_value:
                return items.index(old_value)
            else:
                return None
        elif choice == 'a':
            return -1

        if not choice:
            if old_value:
                return items.index(old_value)
            elif default_index is not None:
                return default_index
            else:
                print("Ничего не выбрано. Попробуйте еще раз!")
                continue

        if  not choice.isnumeric():
            print("Введенное значение не является числом. Попробуйте еще раз!")
            continue

        choice= int(choice) - 1
        if choice >= len(items) or choice < 0:
            print("Выбран некорректный вариант. Попробуйте еще раз!")
            continue

        return choice
    
#определение языка символа
def detect_language_of_letter(char_code: int) -> str|None:
    lat_A = ord("A")
    lat_a = ord("a")
    lat_Z = ord("Z")
    lat_z = ord("z")
    rus_firstcapital = ord("А")
    rus_first_lowercase = ord("а") 
    rus_last_capital = ord("Я")
    rus_last_lowercase = ord("я")
    rus_special_capital = ord("Ё")
    rus_special_lowercase = ord("ё")

    if (lat_A <= char_code <= lat_Z) or (lat_a <= char_code <= lat_z):
            char_lang = "lat"
    elif (rus_firstcapital <= char_code <= rus_last_capital) or (rus_first_lowercase <= char_code <= rus_last_lowercase) or (char_code == rus_special_capital) or (char_code == rus_special_lowercase):
            char_lang= "rus"
    else:
        return None
    
    return char_lang

#определение языка введенного слова
def detect_language(word: str) -> str|None:
    char_code = ord(word[0])
    lang_char= detect_language_of_letter(char_code=char_code)
    if lang_char is not None:
        prev_lang = lang_char
    else:
        return None

    for char in word[1:]:
        lang_char = detect_language_of_letter(ord(char))
        if lang_char is None:
            continue

        if lang_char != prev_lang:
            print("Невозможно определить язык введенного слова.")
            return None
    return prev_lang


#вывод на экран нумерованного списка для выбора
def show_numbered_list(items: list, title: str) -> None:
    #clear_screen()
    print(title.upper())
    for key, item in enumerate(items):
       print(key+1, item, sep=". ")     

    
#функция  очистки экрана
def clear_screen() -> None:
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")

    #ожидание нажатия Enter
def pause() -> None:
    input("\nНажмите Enter для продолжения.")
