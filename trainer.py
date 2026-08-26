import random
from datetime import date, timedelta
from copy import deepcopy

from config import                        *
from storage import  vocabulary, stats, load_json, convert_date_to_string, load, convert_string_to_date, categories
from utils import  input_dialog, answer_dialog, input_number, clear_screen, pause, choose_item, show_numbered_list
from statistic import stats_session_results

DEFAULT_COUNT_WORDS = 5
MAX_COUNTS_WORDS = 20
MIN_COUNTS_WORDS = 5
DEFAULT_MAX_CYCLES = 5
LEARNING_SHARE_FACTOR = 0.5
CONSOLIDATING_SHARE_FACTOR = 0.4
ERROR_SHARE_MAX_SCORE =500
STREAK_SHARE_MAX_SCORE = 50
OVERDUE_SCORE_PER_DAY = 150
TRANSITION_INTERVAL_THRESHOLD_UP = 2
TRANSITION_INTERVAL_THRESHOLD_DOWN = 2 
DIFFICULT_THRESHOLD = 0.4

PRIORITY = "priority"
REQUIRED_CORRECT = "required_correct"
SESSION_ERRORS ="session_errors"

TRANSLATION_MODE = ["английский -> русский", "русский -> английский"]

TRAINER_SETTINGS = {
    "validation": True,
    "required": True,
    "to_lower": True
}

start_stats = {}

#получение списка слов на сессию
def get_learning_words(count_words: int) -> tuple[list[str, ...], int]:
    learning_list = []
    consolidating_list = []
    reviewing_list = []
    additional_consolidating_list = []
    additional_reviewing_list = []
#формирование трех основных и двух дополнительных списка с разными статусами
    for word, values in stats.items():
            match values[STATUS] :
                case "postponed":
                    continue
                case "consolidating":
#в основной список попадут просроченные и трудные слова
                    if (values[NEXT_SHOW] - date.today()).days <= 0 or values[CORRECT] / values[SHOWS] <= DIFFICULT_THRESHOLD:
                        consolidating_list .append((word, values[PRIORITY]))
                    else:
                        additional_consolidating_list.append((word, values[PRIORITY]))
                case "reviewing":
                    if (values[NEXT_SHOW] - date.today()).days <= 0:
                        reviewing_list.append((word, values[PRIORITY]))
                    else:
                        additional_reviewing_list.append((word, values[PRIORITY]))
                case _:
                    learning_list.append((word, values[PRIORITY]))

#сортировка списки по убыванию приоритета
    learning_list.sort(key=lambda item: item[1], reverse=True)
    consolidating_list.sort(key=lambda item: item[1], reverse=True)
    additional_consolidating_list.sort(key=lambda item: item[1], reverse=True)
    reviewing_list.sort(key=lambda item: item[1], reverse=True)
    additional_reviewing_list.sort(key=lambda item: item[1], reverse=True)
    
    length_learning = len(learning_list)
    length_consolidating = len(consolidating_list)
    length_reviewing = len(reviewing_list)
    length_add_consolidating = len(additional_consolidating_list)
    length_add_reviewing = len(additional_reviewing_list)
    count_words = min(length_learning + length_consolidating + length_reviewing + length_add_consolidating + length_add_reviewing, count_words)
    
    #распределение количества слов для каждой группы
    learning_share = round(count_words * LEARNING_SHARE_FACTOR)
    consolidating_share = round(count_words * CONSOLIDATING_SHARE_FACTOR)
    reviewing_share = count_words - (learning_share + consolidating_share)
    required_count = [min(length_learning, learning_share), min(length_consolidating, consolidating_share), min(length_reviewing, reviewing_share), 0, 0]
    vacancies = [learning_share - required_count[0],  consolidating_share - required_count[1], reviewing_share - required_count[2]]
    available_count = [length_learning- required_count[0], length_consolidating - required_count[1], length_reviewing - required_count[2], length_add_consolidating, length_add_reviewing]
#списки из которых берутся недостающие слова
    groups =[(1, 2, 3, 4), (0, 2, 3, 4), (0, 1, 3, 4)]

    for i in range(3):
        while vacancies[i] > 0:
            for group in groups[i]:
                if available_count[group] >= vacancies[i]:
                    required_count[group] += vacancies[i]
                    available_count[group] -= vacancies[i]
                    vacancies[i] =0
#все свободные места распределены
                    break
                else:
                    required_count[group] += available_count[group]
                    vacancies[i] -= available_count[group]
                    available_count[group] =0
                    
    total_list = learning_list[:required_count[0]] + consolidating_list[:required_count[1]] + reviewing_list[:required_count[2]] + additional_consolidating_list[:required_count[3]] + additional_reviewing_list[:required_count[4]]
    
    session_list = [word for word, _ in total_list]
    return (session_list, count_words)

#расчет приоритета 
def calculate_priority() -> None:
    for word, values in stats.items():
        if values[STATUS] == "postponed":
            continue

        
#баллы за статус
        status_score= STATUSES[values[STATUS]][SCORE]
        
#штраф за просроченный срок повторения
        if values[NEXT_SHOW]  is not  None:
            overdue = (values[NEXT_SHOW] - date.today()).days
            overdue_penalty = abs(min(overdue, 0) * OVERDUE_SCORE_PER_DAY)
        else:
            overdue_penalty = 0
        
            #штраф за неверные ответы
        if values[SHOWS] != 0:
            error_ratio = (values[SHOWS] - values[CORRECT]) / values[SHOWS]
            accuracy = values[CORRECT]/values[SHOWS]
            error_share = error_ratio * ERROR_SHARE_MAX_SCORE
        else:
            accuracy = 0
            error_share = 0
        
#бонус за серию верных ответов
        streak_bonus = values[STREAK] * accuracy * STREAK_SHARE_MAX_SCORE
        
        priority =  status_score + overdue_penalty + error_share - streak_bonus
        
        stats[word][PRIORITY] = priority

#установка первоначального числа показов слов
def set_counts_cycles(words_list: list) -> None:
    for word in words_list:
        
        match  stats[word][STATUS]:
            case "new":
                stats[word][REQUIRED_CORRECT] = 2
            case "learning":
                if stats[word][SHOWS] > 3 and (stats[word][STREAK] < 3 or (stats[word][SHOWS]-  stats[word][CORRECT]) > stats[word][CORRECT]):
                    stats[word][REQUIRED_CORRECT] = 3
                else:
                    stats[word][REQUIRED_CORRECT] = 2
            case "consolidating":
                if stats[word][STREAK] < 3 or (stats[word][NEXT_SHOW] ) <= date.today():
                    stats[word][REQUIRED_CORRECT] = 2
                else: 
                    stats[word][REQUIRED_CORRECT]  = 1
            case "reviewing":
                stats[word][REQUIRED_CORRECT] = 1
                
#изменение статуса
def set_new_status(word: str) -> None:   
    shows = stats[word][SHOWS]
    if shows != 0:
        accuracy = stats[word][CORRECT]/shows
    else:
        accuracy = 0
    streak = stats[word][STREAK]
    interval = stats[word][INTERVAL]
    last_wrong = stats[word][LAST_WRONG]
    wrong_count = shows - stats[word][CORRECT]
    status = stats[word][STATUS]
    max_interval = STATUSES[status][INTERVALS][-1] 
    params = STATUSES[status].get(TRANSITION_PARAMS)
    
    statuses_list = [key for key in STATUSES.keys() if key != POSTPONED]
    
    #переход вверх
    
    if status != "reviewing" and shows >= params.get(MIN_SHOWS) and accuracy >= params.get(ACCURACY_THRESHOLD) and interval == max_interval and (status == NEW or streak >= params.get(MIN_STREAK)):
            index = statuses_list.index(status) + 1
        
#переход вниз     
    elif status != "new" and status != "learning" and wrong_count - last_wrong >=params.get(MIN_WRONGS) and streak == 0:    
                index = statuses_list.index(status) - 1
                stats[word][LAST_WRONG] = wrong_count #фиксируем новое значение ошибок
    else:
            return

    stats[word][STATUS] = statuses_list[index]
    #первыое значение списка интервалов для нового статуса
    stats[word][INTERVAL] = STATUSES[stats[word][STATUS]][INTERVALS][0]
                
#функция показа слова из списка
def training_session(session_words: list,  training_params: tuple) -> bool:
    is_session_complete = False
    _, max_shows, translation_mode = training_params
    session_shows = 0
    remaining_cycles = max(stats[word][REQUIRED_CORRECT] for word in session_words)
    print("Начало сессии режима обучения.")
    
    for word in session_words:
        stats[word][SESSION_ERRORS] = 0

    while remaining_cycles != 0:
        random.shuffle(session_words)
        
        for word in session_words: 
            if session_shows >= max_shows:
                break
            if stats[word][REQUIRED_CORRECT] == 0: #слово прошло все циклы
                continue

            translation = vocabulary[word][TRANSLATION]
            stats[word][SHOWS] += 1
            
            if translation_mode:
                prompt_word = word
                correct_answer = translation
            else:
                prompt_word = translation
                correct_answer = word

            user_answer =input_dialog(f"Переведите {prompt_word} ", TRAINER_SETTINGS)
            
            while user_answer is None:            
                if answer_dialog("Вы действительно хотите прервать тренировку?"):
                    print("Тренировка прервана.")
                    return is_session_complete
                else:
                    print("Тренировка продолжена.")
                    user_answer =input_dialog(f"Переведите {prompt_word} ", TRAINER_SETTINGS)    

            if  correct_answer == user_answer:
                print("Ответ верный.")  
                stats[word][STREAK] +=1
                stats[word][CORRECT] += 1    
                stats[word][REQUIRED_CORRECT] -= 1
            else:
                print("Ответ неверный!")
                print(f"Перевод слова {prompt_word} - {correct_answer}")
                stats[word][STREAK] = 0
                stats[word][SESSION_ERRORS] += 1
                
        if session_shows < max_shows:
            remaining_cycles = max(stats[word][REQUIRED_CORRECT] for word in session_words)
        else:
            remaining_cycles = 0

    print("Сессия завершена.")
    return not is_session_complete

#изменение интервала повторения
def get_new_interval(word: str) -> None:
    interval = stats[word][INTERVAL]
    status = stats[word][STATUS]
    max_index = len(STATUSES[stats[word][STATUS]][INTERVALS]) - 1
    min_interval = STATUSES[stats[word][STATUS]][INTERVALS][0]
    current_index = STATUSES[status][INTERVALS].index(interval)
    if status == "new" and current_index == 0:
        stats[word][INTERVAL] =  STATUSES[status][INTERVALS][current_index + 1]
    elif  stats[word][STREAK] >= TRANSITION_INTERVAL_THRESHOLD_UP:
        stats[word][INTERVAL] = STATUSES[status][INTERVALS][min(current_index + 1, max_index)]
    elif stats[word]["incorrect_per_session"] >= TRANSITION_INTERVAL_THRESHOLD_DOWN:
        stats[word][INTERVAL] = STATUSES[status][INTERVALS][max(current_index - 1, 0)]
        print(stats[word]["incorrect_per_session"] )
        print(stats[word][INTERVAL] )

#установка следующей даты повторения
def set_next_show(word: str) -> None:
    interval = stats[word][INTERVAL]
    stats[word][NEXT_SHOW]  = date.today() + timedelta(days=interval)


#установка параметров сессии 
def set_session_params() -> tuple[int, int, bool]|None:
    
#установка количества слов
    prompt = f"Введите количество слов для изучения (5-20) или нажмите Enter, чтобы оставить по умолчанию {DEFAULT_COUNT_WORDS}: "
    count_words = input_number(prompt, MIN_COUNTS_WORDS, MAX_COUNTS_WORDS, DEFAULT_COUNT_WORDS)
    if count_words is None:
        return

    count_words = int(count_words)
    available_count = sum(1 for word in stats if stats[word][STATUS] != "postponed")
    if available_count < count_words:
        print(f"В словаре недостаточно слов. В сессию может быть включено {available_count} слов.")
        if not answer_dialog("Продолжить?"):
            return
        else:
            count_words  = available_count

#расчет минимального числа показов и числа показов по умолчанию
    min_shows = count_words 
    max_shows = count_words * DEFAULT_MAX_CYCLES
    default_shows = int(count_words + 2 * count_words * LEARNING_SHARE_FACTOR + count_words * CONSOLIDATING_SHARE_FACTOR)
    prompt = f"Введите максимальное количество показов за сессию ({min_shows}-{max_shows}) или нажмите Enter, чтобы оставить по умолчанию {default_shows}: "
    shows_limit = input_number(prompt, min_shows, max_shows, default_shows)
    if shows_limit is None:
        return

    shows_limit = int(shows_limit)

    #выбор режима перевода
    back_translation = False
    show_numbered_list(TRANSLATION_MODE, "Выбор направления перевода")
    item = choose_item(items=TRANSLATION_MODE, default_index=1)
    if item is None:
        return
    if item == 1:
        back_translation = True

    return (count_words, shows_limit, back_translation)

#сохранение копии словаря
def save_start_stats(should_save: bool) -> None:
    if should_save:
        start_stats.clear()
        start_stats.update(deepcopy(stats))
    else:
        stats.clear()
        stats.update(start_stats)


#функция запуска режима тренировки
def start_session() -> None:
    clear_screen()
    if not vocabulary:
        print("В словаре нет слов. Тренировка отменена.")
        pause()
        return
    elif not stats:
        print("Отсутствует словарь статистики. Тренировка отменена.")
        pause()
        return
    #сохранение копии словаря до начала тренировки
    save_start_stats(should_save=True)
#получение параметров сессии
    session_params= set_session_params()
    if session_params:
        user_count_words, shows_words, TRANSLATION_MODE = session_params
    else:
        print("Тренировка отменена.")
        pause()
        return
    
    calculate_priority()
    session_list, count_words = get_learning_words(user_count_words)
    
    if not session_list:
        print("Нет слов для изучения.")
        pause()
        return

    set_counts_cycles(session_list)
    is_session_complete = training_session(session_list, session_params)
    if  is_session_complete:
        for word in session_list:
            get_new_interval(word)
            set_new_status(word)
            set_next_show(word)
        if answer_dialog("Вывести статистику по результатам сессии на экран?"):
            stats_session_results(start_stats, session_list)        
    else:
        save_start_stats(should_save=False)
    pause()

