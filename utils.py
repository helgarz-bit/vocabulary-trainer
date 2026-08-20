import os

#функция диалога с ответами "да"\"нет"
def answer_dialog(prompt: str) -> bool:
    while True:
        answer = input(f"{prompt} Введите y/n(д/н): ").strip().lower()
            
        if answer == 'y' or answer == 'д':
            return True
        elif answer == 'n' or 'н':
            return False
        print("Введен недопустимый вариант. Попробуйте еще раз!")

#управление действием
def what_to_do(repeat: bool) -> str:
    prompt = ""
    if repeat:
        prompt = "Введите r для повторения действия."
    while True:
        do = input(f'Введите m - вернуться в меню\n{prompt}')
        if do == "m":
            return "return"
        elif repeat and do == "r":
            return 'r'
        else:
            print("Введена недопустимая команда. Попробуйте еще раз!")

#функция проверки ввода слова
def check_valid(value: str) -> bool:
#проверка первого символа
    char = value[0]
    if not char.isalpha():
        print("Слово должно начинаться с буквы! ")
        return

    prev_char = ""
    for char in value[1:]:
        if char.isalpha():
            continue
        elif char in {" ", "'", "-"}:
            if prev_char :
                return False
            else:
                prev_char = char
        else:
            return False
    return True
    
#функция обработки ввода  слова
def input_dialog(prompt: str,settings: dict, old_value: str|None = None) -> str|None:
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
def choose_item(items: list, default_index: int, old_value: str|None =None) -> int|None:

    while True:
        choice  = input("Выберите значение из списка. q - отмена")

        if choice == 'q':
            if old_value:
                return items.index(old_value)
            else:
                return None

        if not choice:
            if old_value:
                return items.index(old_value)
            else:
                return default_index

        if  not choice.isnumeric():
            print("Введенное значение не является числом. Попробуйте еще раз!")
            continue

        if not any (choice == item[0] for item in items):
            print("Выбран некорректный вариант. Попробуйте еще раз!")
            continue

        return int(choice)
    

#определениеязыка символа
def detect_language_of_letter(char: str) -> str|None:
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

    if (lat_A < char< lat_Z) or (lat_a < char< lat_z):
            char_lang = "lat"
    elif (rus_firstcapital < char< rus_last_capital) or (rus_first_lowercase < char< rus_last_lowercase) or (char== rus_special_capital) or (char== rus_special_lowercase):
            char_lang= "rus"
    else:
        return None
    
    return char_lang

#определение языка введенного слова
def detect_language(word: str) -> str|None:
    char_code = ord(word[0])
    lang_char= detect_language_of_letter(char=char_code)
    if lang_char is not None:
        prev_lang = lang_char

    for char in word[1:]:
        lang_char = detect_language_of_letter(ord(char))
        if lang_char is None:
            continue

        if lang_char != prev_lang:
            print("Невозможно определить язык введенного слова.")
            return None
    return prev_lang

#функция  очистки экрана
def clear_screen() -> None:
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")

#ожидание нажатия ENter
def pause() -> None:
    input("\nНажмите Enter для продолжения.")
