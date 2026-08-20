from storage import vocabulary, stats, categories
from utils import answer_dialog, input_dialog, pause, clear_screen, what_to_do, detect_language
from config import *
from statistic import show_stats_word
from display  import show_table, prepare_data_to_print

#вывод списка категорий
def show_category(prompt: str|None =None) -> None:
    clear_screen()
    if not prompt:
        prompt = "Выберите категорию из списка."
    print(f"{prompt} \na - добавить новую категорию \n q - отмена")
    for index in range(len(categories)):
        print(f"{index+1} - {categories[index]}")


#выбор и назначение категории
def choose_category(old_category: str|None =None) -> int|None:    
    while True:
        choice = input("Введите номер категории: ").strip()
        if choice == 'q': #выбор отменен
            if old_category is None:
                return None 
            else:
                return categories.index(old_category)
        elif choice == 'a':
            add_category()
            show_category()
            continue
        elif not choice: #пустая строка        
            if old_category is not None: #страя категория при редактировании слова
                return categories.index(old_category)
            else:
                return 0 #возвращаем категорию по умолчанию
        #строка не пустая
        if not choice.isnumeric(): #введенное значение не число
            print("Введенное значение не является числом. Попробуйте еще раз!")
            continue
        else:
            choice = int(choice)
#проверяем диапазон
            if choice < 1 or choice > len(categories):    
                print("Введенное значение вне допустимого диапазона")
                continue

#возвращаем индекс        
        return choice    -1

#установка категории для слова
def set_category(old_category: str|None =None) -> str:
    if  old_category is not None:
        prompt = 'Выберите категорию или нажмите "Enter", чтобы оставить категорию без изменения.'
    else:
        prompt = None
#выбираем из списка категорий
    show_category(prompt)
    index_cat = choose_category(old_category)
    
    if index_cat is None:
        category = DEFAULT_CATEGORY
    else:
        category= categories[index_cat]

    return category

#получение значения категории
def input_category(old_category: str|None =None) -> str|None:
    category = input_dialog("Введите название категории ", settings=FIELDS[CATEGORY][SETTINGS], old_value=old_category)

    if category is None:
        return None

    #проверка на уникальность
    if category in categories:
        print(f"Категория {category} уже существует.")
        return None

    return category

#переназначение категории в словаре слов
def appointment_category(old_category: str, new_category: str) -> None:
    for word, values in vocabulary.items():
        if values[CATEGORY] == old_category:
            values[CATEGORY] = new_category

#добавление новой категории
def add_category() -> None:
    print("Добавление новой категории. Для отмены введите q")
    category = input_category()
    if category is None:
        print("Добавление категории отменено.")
        return

    categories.append(category)
    print(f"Категория {category} успешно добавлена.")
  
#редактирование категории
def edit_category() -> None:
    print("Редактирование категории.")
    show_category()
    index_cat = choose_category()
    if index_cat is None:
        print("Редактирование категории отменено.")
        return

    if index_cat == 0:
        print('Редактирование категории "по умолчанию" невозможно.')
        return

    old_category = categories[index_cat]
    print(f"Редактирование категории {old_category}")

    new_category = input_category(old_category)
    if new_category is None:
        print("редактирование категории отменено.")
        return
    if new_category != old_category:
        categories[index_cat] = new_category
        print(f"Редактирование категории завершено. Новое значение категории - {new_category}")
    else:
        print(f"Категория {old_category} не изменена.")

#переназначение измененной категории в словаре слов
    appointment_category(old_category, new_category)

#удаление категории
def delete_category() -> None:
    print("Удаление категории.")
    show_category()
    index_cat = choose_category()
    if index_cat is None:
        print("Удаление категории отменено.")
        return
    if index_cat == 0:
        print('Удаление категории "по умолчанию" невозможно.')
        return

    category = categories[index_cat]
    if answer_dialog(f"Вы действительно хотите удалить категорию {categories[index_cat]}?"):
        del categories[index_cat]
        print(f"Категория {category} удалена.")
    else:       
        print(f"Удаление категории {category} отменено.")

    appointment_category(category, DEFAULT_CATEGORY)

#функция инициализации статистики
def set_stats(word: str) -> None:
    stats[word] = {
        SHOWS: 0, 
        CORRECT: 0, 
        STREAK: 0, 
        STATUS: NEW, 
        NEXT_SHOW: None, 
    INTERVAL: STATUSES[NEW][INTERVALS][0],
        LAST_WRONG: 0}

#формирование текста запроса
def form_prompt(field_name: str, is_edit: bool) -> str:
    if is_edit:
        prompt = 'Введите новое значение или нажмите "Enter", чтобы оставить значение без изменения.'
    else:
        prompt = f"Введите {FIELDS[field_name][PROMPT]}"

    return prompt
    
#проверка существования записи в словаре
def check_existence_word        (word: str, lang: str) -> str|None:
    if lang == "lat":
        if word in vocabulary:
             return word
        else:
            return None

    for  key, values in vocabulary.items():
        if values[TRANSLATION] == word:
            return key

    return None

#получение корректного ключа
def get_word_key(must_be: bool, old_word: str|None =None) -> str|None:
    prompt = form_prompt(WORD, is_edit=bool(old_word))
    word = input_dialog(prompt, settings=FIELDS[WORD][SETTINGS], old_value=old_word)

    if word is None:
        return None
#определение языка введенного слова
    lang_word = detect_language(word)
    if lang_word is None:
        print("Некорректно введенное слово.") 
        return None

    if not must_be and lang_word == "rus":
        print("Слово должно быть введено латиницей.")
        return None

    key_word = check_existence_word(word, lang_word)
    if key_word is None:
        if must_be:
            print(f"Слово {word} не найдено в словаре.")
            return None
        else:
            return word
    else:
            if not must_be:
                print(f"Слово {word} уже существует.")
                return None
            else:
                return key_word


#функция получения значений записи словаря
def get_values(old_word: str|None =None) -> dict|None:
    old_values = {}
    values = {}
    
    if old_word is not None: #редактирование
        old_values = {TRANSLATION: vocabulary[old_word][TRANSLATION], EXAMPLE: vocabulary[old_word][EXAMPLE]}

    for field_name, settings in FIELDS.items():
        if field_name == WORD or field_name == CATEGORY:
            continue
         
        if old_word is not None:
            print(f'{settings[PROMPT]}- текущее значение: {old_values[field_name]}.')
            
        prompt = form_prompt(field_name, is_edit=bool(old_word))

        value = input_dialog(prompt=prompt, settings=settings[SETTINGS], old_value=old_values.get(field_name))

        if value is None: #пользователь отменил операцию
            return None
        
        values[field_name] = value
    return values
        
#функция добавления слова в словарь
def add_word() -> None:
    print("Добавление слова в словарь.")
    word = get_word_key(must_be=False)
    if word is None:
        print("Добавление нового слова отменено.")
        return
#получение значений остальных полей
    values = get_values()
    if  values is None:
        print("Добавление нового слова отменено.")
        return

    vocabulary[word] = values
    #назначение категории
    
    vocabulary[word][CATEGORY] = set_category()
    
    set_stats(word)
    print(f"Слово  {word} успешно добавлено в словарь.")


    #функкция редактирования записи
def edit_word() -> None:
    print("Редактирование записи словаря.")
    word = get_word_key(must_be=True)

    if word is None:
        print("Редактирование отменено.")
        return
    
    new_word = get_word_key(must_be=False, old_word=word)

    if new_word is None:
            print("редактирование отменено.")
            return
    
    values = get_values(word)
    if values is None:
        print("Редактирование слова отменено.")
        return
#сохраним старрый перевод и категорию
    old_translation = vocabulary[word][TRANSLATION]
    old_category = vocabulary[word][CATEGORY]
    #записываем новые значения в словарь
    vocabulary[new_word] = values
    #переназначение категории
    category = set_category(old_category=old_category)
    vocabulary[new_word][CATEGORY] = category
#если изменили слово
    if word != new_word:
        #старую запись и статистику удаляем 
        del vocabulary[word]
        del stats[word]
#если изменилось слово или перевод
    if word != new_word or old_translation != values[TRANSLATION]:
        #обнуляем статистику для слова
                set_stats(new_word)

    print("Редактирование слова завершено.")            

    
#функция удаления записи
def delete_word() -> None:
    print("Удаление записи словаря.")
    word = get_word_key(must_be=True)

    if word is None:
        print("Удаление отменено.")
        return

    if answer_dialog(f"Вы действительно хотите удалить слово {word}?"):
        del vocabulary[word]
        del stats[word]
        print(f"Слово {word} удалено из словаря.")
    else:
        print("Удаление отменено.")    
    
#функция поиска слова 
def find_word() -> None:
    print("Поиск записи слова в словаре.")
    word = get_word_key(must_be=True)

    if word is None:
        print("Поиск слова отменен")
        return
    
    show_table(title=f"Карточка слова {word}", data=(vocabulary, word))
    show_table(title=f"статистика изучения слова {word}", data=(stats, word))
#функция вывода списка всех слов из словаря
def show_all_words() -> None:    
    headers = [["Английское слово"], ["Перевод"], ["Категория"], ["Пример"]]
    show_table(title="Список слов словаря", data=vocabulary, headers=headers)


#поиск по категории
#def search_by_category():

#начальная функция
def manager_dict(action: str) -> None:
    repeat = True
    while True:
        clear_screen()
        match action:
            case "add":
                add_word()
            case "edit":
                edit_word()
            case "delete":
                delete_word()
            case "find":
                find_word()
            case "all":
                repeat = False
                show_all_words()
            case "add_cat":
                add_category()
            case "edit_cat":
                edit_category()
            case "delete_cat":
                delete_category()
            case "return":
                break
    
        do =what_to_do(repeat)
        if do != 'r':
            action = do

        #проверка работы модуля
if __name__ == "__main__":
    pass
    