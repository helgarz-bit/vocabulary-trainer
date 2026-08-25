from storage import vocabulary, stats, categories
from utils import answer_dialog, input_dialog, pause, clear_screen, what_to_do, detect_language, show_numbered_list, choose_item
from config import *

from display  import show_table, prepare_data_to_print


     

#установка категории для слова
def set_category(is_add_new: bool =False, old_category: str|None =None) -> str:
    print("\n")
    if  old_category is not None:
        message= f'текущая категория - {old_category}. Нажмите "Enter", чтобы оставить категорию без изменения. \na - добавление новой категории'
    elif is_add_new:
        message= "a - добавление новой категории"
    else: 
        message = None

    show_numbered_list(categories, "Выбор категории")
    index_cat = choose_item(categories, default_index=0, old_value=old_category, message=message)
    is_break = False
    while not is_break:
        if index_cat is None:
            category = DEFAULT_CATEGORY
            is_break = True
        elif index_cat == -1:
            add_category()
            show_numbered_list(categories, "Выбор категории")
            index_cat = choose_item(categories, default_index=0, old_value=old_category, message=message)
        else:
            category= categories[index_cat]
            is_break = True

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
    show_numbered_list(categories, "Список категорий")
    index_cat = choose_item(categories, default_index=0)
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
    show_numbered_list(categories, "Список категорий")
    index_cat = choose_item(categories, default_index=0)
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

#вывод списка категорий
def manager_categories() -> None:
    while True:
        show_numbered_list(categories, "Список категорий")
        print("a - добавить категорию")
        print("e - редактировать категорию")
        print("d - удалить категорию")
        print("m - возврат в меню")
        choice = input("Выберите дйствие: ")
        clear_screen()
        if choice== 'a':
            add_category()
        elif choice == 'e':
            edit_category()
        elif choice == 'd':
            delete_category()
        elif choice == 'm':
            return
        else:
            print("Введена неизвестная команда. Попробуйте еще раз!")
        


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
def form_prompt(field_name: str, is_edit: bool, value: str|None =None) -> str:
    if is_edit:
        prompt = f'{FIELDS[field_name][PROMPT]} - текущее значение: {value}\nВведите новое значение или нажмите "Enter", чтобы оставить значение без изменения.'
    else:
        prompt = f"Введите {FIELDS[field_name][PROMPT]}"

    return prompt
    
#проверка существования записи в словаре
def check_existence_word        (word: str, lang: str) -> list:
    words = []
    if lang == "lat":
        if word in vocabulary:
            words.append(word)
            return words
        
    for  key, values in vocabulary.items():
        if values[TRANSLATION] == word:
            words.append(key)
    return words

#получение корректного ключа
def get_word_key(must_be: bool, old_word: str|None =None) -> str|None:
    prompt = form_prompt(WORD, is_edit=bool(old_word), value=old_word)
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

    keys_words = check_existence_word(word, lang_word)
    
    if not keys_words:
        if must_be:
            print(f"Слово {word} не найдено в словаре.")
            return None
        else:
            return word
    else:
            if not must_be and (word != old_word):
                print(f"Слово {word} уже существует.")
                return None
            else:
                if len(keys_words) > 1:
                    print(f"Найдено {len(keys_words)} записей с переводом '{word}'.")
                    #words_list = [(str(key + 1), value) for key, value in enumerate(keys_words)]
                    show_numbered_list(keys_words, "Выберите слово из списка")
                    key = choose_item(keys_words)
                    if key is None:
                                    return None            
                    print(f"Выбрано слово {keys_words[key]}")
                    return keys_words[key]
                
                key = keys_words.pop()
                return key


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
            old_value  = old_values[field_name]
        else:
            old_value = None
            #print(f'{settings[PROMPT]}- текущее значение: {old_values[field_name]}.')
            
        prompt = form_prompt(field_name, is_edit=bool(old_word), value=old_value)

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
    
    vocabulary[word][CATEGORY] = set_category(is_add_new=True)
    
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
    category = set_category(is_add_new=True, old_category=old_category)
    vocabulary[new_word][CATEGORY] = category
#если изменили слово
    if word != new_word:
        #старую запись и статистику удаляем 
        del vocabulary[word]
        del stats[word]
#если изменилось слово или перевод
    if word != new_word:
        #обнуляем статистику для слова
                set_stats(new_word)
    elif old_translation != values[TRANSLATION]:
        answer = answer_dialog(prompt=f"Обнулить статистику слова {new_word}")
        if answer:
            set_stats(new_word)
    print(f"Редактирование слова {word} завершено.")            

    
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
def search_by_category():
    show_numbered_list(categories, "Список категорий")
    choice = choose_item(categories, default_index=0)
    if choice == None:
        return

    rows = []
    selected_values = [word for word, values in vocabulary.items() if values[CATEGORY] == categories[choice] ]
    for word in selected_values:
        row = (word, vocabulary[word][TRANSLATION], vocabulary[word][EXAMPLE])
        rows.append(row)

    headers = [["English word"], ["Перевод"], ["Пример"]]
    title = f"Слова категории {categories[choice]}"

    show_table(title=title, data=rows, headers=headers)
    

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
            case "find_by_cat":
                repeat  = True
                search_by_category()

            case "return":
                break
    
        do =what_to_do(repeat)
        if do != 'r':
            action = do

        #проверка работы модуля
if __name__ == "__main__":
    pass
    