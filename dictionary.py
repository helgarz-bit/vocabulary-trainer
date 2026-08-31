from storage import vocabulary, stats, categories
from utils import answer_dialog, input_dialog, pause, clear_screen, what_to_do, detect_language, show_numbered_list, choose_item
from config import *
from display  import show_table 


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


#установка категории для слова
def set_category(is_add_new: bool =False, old_category: str|None =None) -> str|None:
    """Выводит список категорий, позволяет выбрать или добавить категорию.
    
    При редактировании существующей записи словаря текущую категорию 
    можно оставить без изменения нажатием клавишши Enter.
    Пользователь может добавить новую категорию и затем выбрать ее из обновленного списка.
    
    Args:
        is_add_new: Определяет доступно ли добавление новой категории при выборе категории.
        old_category: Текущая категория. используемая при редактировании.
        Если указана, пользователь может оставить ее без изменения.

    Returns:
    Возвращает выбранную категорию или None, если пользователь отменил выбор.
        """
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
            return None
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
    category = input_dialog("Введите название категории ", settings=FIELDS[CATEGORY][SETTINGS])

    if category is None:
        return None

    #проверка на уникальность
    if category in categories and category != old_category:
        print(f"Категория {category} уже существует.")
        return None

    return category

#переназначение категории в словаре слов
def reassign_category(old_category: str, new_category: str) -> None:
    for values in vocabulary.values():
        if values[CATEGORY] == old_category:
            values[CATEGORY] = new_category

#добавление новой категории
def add_category() -> bool|None:
    print("Добавление новой категории.\nq - отмена")
    category = input_category()
    if category is None:
        return True

    categories.append(category)
    print(f"Категория {category} успешно добавлена.")
  
#редактирование категории
def edit_category() -> bool|None:
    print("Редактирование категории.")
    show_numbered_list(categories, "Список категорий")
    index_cat = choose_item(categories, default_index=0)
    if index_cat is None:
        return True

    if index_cat == 0:
        print('Редактирование категории "по умолчанию" невозможно.')
        return

    old_category = categories[index_cat]
    print(f"Редактирование категории {old_category}")

    new_category = input_category(old_category)
    if new_category is None:
        return True
    if new_category != old_category:
        categories[index_cat] = new_category
        print(f"Редактирование категории завершено. Новое значение категории - {new_category}")
    else:
        print(f"Категория {old_category} не изменена.")

#переназначение измененной категории в словаре слов
    reassign_category(old_category, new_category)

#удаление категории
def delete_category() -> bool|None:
    print("Удаление категории.")

    show_numbered_list(categories, "Список категорий")
    index_cat = choose_item(categories, default_index=0)
    if index_cat is None:
        return True
    if index_cat == 0:
        print('Удаление категории "по умолчанию" невозможно.')
        return

    category = categories[index_cat]
    if answer_dialog(f"Вы действительно хотите удалить категорию {categories[index_cat]}?"):
        del categories[index_cat]
        print(f"Категория {category} удалена.")
    else:       
        return True

    reassign_category(category, DEFAULT_CATEGORY)

#менеджер категорий
def manager_categories() -> None:
    """Управляет категориями словаря.
    
    Выводит список категорий, позволяет добавлять, редактировать
    и удалять категории, а ткже возвращаться в меню.
    """
    cancel  = False
    while True:
        clear_screen()
        print("Управление категориями".upper())
        show_numbered_list(categories, "Список категорий")
        print("a - добавить категорию")
        print("e - редактировать категорию")
        print("d - удалить категорию")
        print("m - возврат в меню")
        choice = input("Выберите дйствие: ")
        
        if choice == 'a':
            cancel = add_category()
            action = "add"
        elif choice == 'e':
            cancel = edit_category()
            action = "edit"
        elif choice == 'd':
            cancel = delete_category()
            action = "delete"
        elif choice == 'm':
            return
        else:
            print("Введена неизвестная команда. Попробуйте еще раз!")
        
        if cancel:
            print(f"{ACTIONS[action][PROMPT]} категории отменено.")
            

#формирование текста запроса
def form_prompt(field_name: str, is_edit: bool, value: str|None =None) -> str:
    if is_edit:
        prompt = f'{FIELDS[field_name][PROMPT]} - текущее значение: {value}\nВведите новое значение или нажмите "Enter", чтобы оставить значение без изменения.\nq - отмена'
    else:
        prompt = f"Введите {FIELDS[field_name][PROMPT]}\nq - отмена"

    return prompt
    
#проверка существования записи в словаре
def find_words_matches(word: str, lang: str) -> list[str]:
    """Ищет слово в словаре, возвращает список найденных слов.
    Для слов, написанных латиницей, ищет слово среди
    ключей словаря. Для слов на кириллице ищет
    слово среди переводов и возвращает список соответствующих ключей
    
    Args:
        word: Слово, наличие которого нужно проверить.
        lang: Язык искомого слова.
        
    Returns:
        Список слов, соответствующий искомому значению. 
         Если совпадений нет, возвращается пустой список. 
         """
    
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
    """Получает слово от пользователя и определяет по нему ключ в словаре
    Контролирует проверку корректности введенного слова,
    определение языка, ищет соответствующие записи в словаре.
    В зависимости от параметра must_to_be функция либо 
    требует наличия записи в словаре, либо проверяет отсутствие 
    нового слова.
    Если введен перевод, которому соответствует несколько слов, предлагает
     пользователю выбрать нужное слово.
     
     Args:
        must_to_be: Определяет режим поиска: если True, слово должно существовать в словаре.
        Если False - слова не должно быть в словаре, за исключением редактирования существующего
        слова, переданного в old_word.
        old_word: Исходное слово при редактировании записи, используется для того,
        чтобы разрешить оставить текущее слово без изменения.
        
    Returns:
    Ключ найденного или введенного слова. Возвращает None, если ввод
    отменен или не пройдено одно из услови проверки..
    """
    prompt = form_prompt(WORD, is_edit=old_word is not None, value=old_word)
    word = input_dialog(prompt, settings=FIELDS[WORD][SETTINGS], old_value=old_word)

    if word is None:
        return None
#определение языка введенного слова
    lang_word = detect_language(word)
    if lang_word is None:
        print("Некорректно введенное слово.") 
        return None

    if not must_be and lang_word == "rus":
        print("Слово должно быть введено латинскими буквами.")
        return None

    keys_words = find_words_matches(word, lang_word)
    
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
    """Получает значения полей слова от пользователя.
    При редактировании текущие значения полей используются 
    как значения по умолчанию.
    Поля слова и категории пропускаются, так как они обрабатываются отдельно.
    
    Args:
        old_word: Ключ для редактируемого слова. 
        Если значение не указано, значения полей запрашиваются для нового слова.
        
    Returns:
        Словарь с введенными значениями полей или None, если
        пользователь отменил операцию.
        """
    old_values = {}
    values = {}
    
    if old_word is not None: #редактирование
        old_values = vocabulary[old_word]

    for field_name, settings in FIELDS.items():
        if field_name == WORD or field_name == CATEGORY:
            continue
         
        if old_word is not None:
            old_value  = old_values[field_name]
        else:
            old_value = None
        prompt = form_prompt(field_name, is_edit=bool(old_word), value=old_value)

        value = input_dialog(prompt=prompt, settings=settings[SETTINGS], old_value=old_values.get(field_name))

        if value is None: #пользователь отменил операцию
            return None
        
        values[field_name] = value
    return values
        
#добавление слова в словарь
def add_word() -> bool|None:
    """Запрашивает слово, значения для его полей  и категорию. 
    Затем создает для слова статистику. Ввод слова можно отменить на любом этапе.
    
    
    Returns:
        True если пользователь отменил операцию.
        None, если добавление прошло успешно.
        """
    print("Добавление слова в словарь.")
    word = get_word_key(must_be=False)
    if word is None:
        return True
#получение значений остальных полей
    values = get_values()
    if  values is None:
        return True

    vocabulary[word] = values
    #назначение категории
    category = set_category(is_add_new=True)
    if category is None:
        return True

    vocabulary[word][CATEGORY] = category
    
    set_stats(word)
    print(f"Слово  {word} успешно добавлено в словарь.")


    #редактирование записи
def edit_word() -> bool|None:
    """Редактирует существующую запись в словаре.
    Позволяет изменить слово, значения его полей и категорию.
    Если изменяется само слово, предыдущая статистика удаляется и создается заново для нового слова.
    При
    изменениии перевода решение о сбросе статистики предоставляется пользователю. В остальных случаях статистика сохраняется.
    Returns:
        True, если пользователь отменил редактирование
        None, если редактирование завершилось успешно.
        """
    print("Редактирование записи словаря.")
    word = get_word_key(must_be=True)

    if word is None:
        return True
    
    new_word = get_word_key(must_be=False, old_word=word)

    if new_word is None:
            return True
    
    values = get_values(word)
    if values is None:
        return True
#сохранение старого перевода и категории
    old_translation = vocabulary[word][TRANSLATION]
    old_category = vocabulary[word][CATEGORY]

    #переназначение категории   
    category = set_category(is_add_new=True, old_category=old_category)
    
    if category is None:
           return True     
        
    #запись новых значений в словарь
    vocabulary[new_word] = values
    vocabulary[new_word][CATEGORY] = category
#если изменили слово
    if word != new_word:
        print(f"Слово {word} изменено. Статистика его изучения будет сброшена.")
        del vocabulary[word]
        del stats[word]
#если изменилось слово или перевод
    if word != new_word:
        #обнуление статистики для слова
                set_stats(new_word)
    elif old_translation != values[TRANSLATION]:
        if answer_dialog(prompt=f"Обнулить статистику слова {new_word}"):
            set_stats(new_word)
            print(f"Статистика слова {new_word} обнулена.")
        else:
            print(f"Статистика слова {new_word} сохранена.")
    print(f"Редактирование слова {new_word} завершено.")            

    
#функция удаления записи
def delete_word() -> bool|None:
    print("Удаление записи словаря.")
    word = get_word_key(must_be=True)

    if word is None:
        return True

    if answer_dialog(f"Вы действительно хотите удалить слово {word}?"):
        del vocabulary[word]
        del stats[word]
        print(f"Слово {word} удалено из словаря.")
    else:
        return True
    
#функция поиска слова 
def find_word() -> bool|None:
    print("Поиск записи слова в словаре.")
    word = get_word_key(must_be=True)

    if word is None:
        return True
    
    show_table(title=f"Карточка слова {word}", data=(vocabulary, word))
    show_table(title=f"статистика изучения слова {word}", data=(stats, word))

#функция вывода списка всех слов из словаря
def show_all_words() -> None:    
    rows = []
    headers = [["English word"], ["Перевод"], ["Категория"], ["Пример"]]
    for word, values in vocabulary.items():
        row = (word, values[TRANSLATION], values[CATEGORY], values[EXAMPLE])
        rows.append(row)
    show_table(title="Список слов словаря", data=rows, headers=headers)


#поиск по категории
def search_by_category() -> bool|None:
    print("Поиск слов по выбранной категории")
    show_numbered_list(categories, "Список категорий")
    choice = choose_item(categories, default_index=0)
    if choice == None:
        return True

    rows = []
    selected_values = [word for word, values in vocabulary.items() if values[CATEGORY] == categories[choice] ]
    if not selected_values:
        print(f"В категории {categories[choice]} нет записей.")
        return 

    for word in selected_values:
        row = (word, vocabulary[word][TRANSLATION], vocabulary[word][EXAMPLE])
        rows.append(row)

    headers = [["English word"], ["Перевод"], ["Пример"]]
    title = f"Слова категории {categories[choice]}"

    show_table(title=title, data=rows, headers=headers)
    

#начальная функция
def manager_dict(action: str) -> None:
    """Управляет операциями со словарем в зависимости от выбранного действия.
    Запускает добавление, редактирование, удаление и поиск слов, выводит
    весь словарь и поиск по категории. После
    завершения операции предлагает продолжить работу или вернуться в меню.
    
    Args:
        action: Код операции, которую необходимо выполнить.
        """
    repeat = True
    cancel = False
    while True:
        clear_screen()
        match action:
            case "add":
                cancel = add_word()
            case "edit":
                cancel = edit_word()
            case "delete":
                cancel = delete_word()
            case "find":
                cancel = find_word()
            case "all":
                repeat = False
                show_all_words()
            case "find_by_cat":
                repeat  = True
                cancel = search_by_category()

            case "return":
                break
    
        if cancel:
            print(f"{ACTIONS[action][PROMPT].capitalize()} отменен{ACTIONS[action]["ending"]}")
            pause()
            return
        action=what_to_do(repeat, action)
        
        