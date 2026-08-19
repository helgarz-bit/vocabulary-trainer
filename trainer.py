import random
from datetime import date, timedelta
from copy import deepcopy

from config import                        *
from storage import  vocabulary, stats
from utils import  input_dialog, answer_dialog, input_number, clear_screen, pause
from display import show_table

DEFAULT_COUNT_WORDS = 5
MAX_COUNTS_WORDS = 20
DEFAULT_MAX_SHOWS = 40
MIN_COUNTS_WORDS = 5
DEFAULT_CYCLES = 3
LEARNING_SHARE_FACTOR = 0.4
CONSOLIDATING_SHARE_FACTOR = 0.5
ERROR_SHARE_MAX_SCORE = 400
STREAK_SHARE_MAX_SCORE = 100
OVERDUE_MAX_SCORE = 150
TRANSITION_INTERVAL_THRESHOLD_UP = 2
TRANSITION_INTERVAL_THRESHOLD_DOWN = 2 

TRAINER_SETTINGS = {
    "validation": True,
    "required": True,
    "to_lower": True
}

start_stats = {}

#получение списка слов на сессию
def get_learning_words(count_words: int) -> tuple:
    learning_list = []
    consolidating_list = []
    reviewing_list = []
#формируем 3 списка с разными статусами
    for word, values in stats.items():
            match values[STATUS] :
                case "postponed":
                    continue
                case "consolidating":
                    consolidating_list .append((word, values["priority"]))
                case "reviewing":
                    reviewing_list.append((word, values["priority"]))
                case _:
                    learning_list.append((word, values["priority"]))

    
    lenth_learning = len(learning_list)
    lenth_consolidating = len(consolidating_list)
    lenth_reviewing = len(reviewing_list)
    count_words = min(lenth_learning + lenth_consolidating + lenth_reviewing, count_words)
    
#сортируем списки по убыванию приоритета
    learning_list.sort(key=lambda item: item[1], reverse=True)
    consolidating_list.sort(key=lambda item: item[1], reverse=True)
    reviewing_list.sort(key=lambda item: item[1], reverse=True)
    
    #распределяем количество слов для каждой группы
    learning_share = round(count_words * LEARNING_SHARE_FACTOR)
    consolidating_share = round(count_words * CONSOLIDATING_SHARE_FACTOR)
    reviewing_share = count_words - (learning_share + consolidating_share)
    required_count = [min(lenth_learning, learning_share), min(lenth_consolidating, consolidating_share), min(lenth_reviewing, reviewing_share)]
    vacancies = [learning_share - required_count[0],  consolidating_share - required_count[1], reviewing_share - required_count[2]]
    available_count = [lenth_learning- required_count[0], lenth_consolidating - required_count[1], lenth_reviewing - required_count[2]]
    groups =[(1, 2), (0, 2), (0, 1)]

    for i in range(3):
        if vacancies[i] > 0:
            addition = min(vacancies[i], available_count [groups[i][0]])
            remaining_counts = vacancies[i]  - addition 
            required_count[groups[i][0]] += addition
            required_count[groups[i][1]] += remaining_counts

    total_list = learning_list[:required_count[0]] + consolidating_list[:required_count[1]] + reviewing_list[:required_count[2]]
    
    session_list = [word for word, _ in total_list]
        
    return (session_list, count_words)

#расчет приоритета 
def calculate_priority() -> None:
    for word, values in stats.items():
        if values[STATUS] == "postponed":
            continue

        priority = 0     
#баллы за статус
        status_score= STATUSES[values[STATUS]][SCORE]
#штраф за просроченный срок повторения
        if values[NEXT_SHOW]  is not  None:
            overdue = (values[NEXT_SHOW] - date.today()).days
            overdue_penalty = abs(min(overdue, 0) * OVERDUE_MAX_SCORE)
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
        
        stats[word]["priority"] = priority

#установка первоначального числа циклов
def set_counts_cycles(words_list: list) -> None:
    for word in words_list:
        
        match  stats[word][STATUS]:
            case "new":
                stats[word]["planed_cycles"] = 2
            case "learning":
                if stats[word][SHOWS] > 3 and (stats[word][STREAK] < 3 or (stats[word][SHOWS]-  stats[word][CORRECT]) > stats[word][CORRECT]):
                    stats[word]["planed_cycles"] = 3
                else:
                    stats[word]["planed_cycles"] = 2
            case "consolidating":
                if stats[word][STREAK] < 3 or (stats[word][NEXT_SHOW] ) <= date.today():
                    stats[word]["planed_cycles"] = 2
                else: 
                    stats[word]["planed_cycles"]  = 1
            case "reviewing":
                stats[word]["planed_cycles"] = 1
                
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
    if shows >= params.get(MIN_SHOWS) and accuracy >= params.get(ACCURACY_THRESHOLD) and interval == max_interval and (status == NEW or streak >= params.get(MIN_STREAK)):
        index = min(statuses_list.index(status) + 1, len(statuses_list))
        
#переход вниз     
    elif status != "new" and status != "learning":
        if wrong_count - last_wrong >=params.get(MIN_WRONGS) and streak == 0:    
            index = min(statuses_list.index(status), 0)
        stats[word][LAST_WRONG] = wrong_count #фиксируем новое значение ошибок
    else:
        return

    stats[word][STATUS] = statuses_list[index]
    #первыое значение списка интервалов для нового статуса
    stats[word][INTERVAL] = STATUSES[stats[word][STATUS]][INTERVALS][0]
                
#функция показа слова из списка
def training_session(learning_list: list, session_stats: dict) -> bool|None:
    is_show_stats = True
    print("Начало сессии режима обучения.")
    
    for  cycle in range(DEFAULT_CYCLES):
        random.shuffle(learning_list)
        
        for word in learning_list: 
            if session_stats[SHOWS] > DEFAULT_MAX_SHOWS:
                break
            if stats[word]["planed_cycles"] < cycle + 1: #слово прошло все циклы
                continue
            translation = vocabulary[word][TRANSLATION]
            stats[word]["incorrect_per_session"] = 0
            
            stats[word][SHOWS] += 1 #увеличиваем счетчик показов слова
            word_answer =input_dialog(f"Переведите {word} ", TRAINER_SETTINGS)
            session_stats[SHOWS] +=1
            while word_answer is None:            
                if answer_dialog("Вы действительно хотите прервать тренировку?"):
                    print("Тренировка прервана.")
                    return not is_show_stats
                else:
                    print("Тренировка продолжена.")
                    word_answer =input_dialog(f"Переведите {word} ", TRAINER_SETTINGS)    
            if  translation == word_answer:
                print("Ответ верный.")  
                stats[word][STREAK] +=1
                stats[word][CORRECT] += 1
                session_stats[CORRECT] +=1
            else:
                print("Ответ неверный!")
                print(f"Перевод слова {word} - {translation}")
                stats[word][STREAK] = 0
                stats[word]["incorrect_per_session"] += 1
                #добавляем еще один показ в текущей сессии
                if  stats[word]["planed_cycles"] < DEFAULT_CYCLES:
                    stats[word]["planed_cycles"] += 1
                
    print("Сессия завершена.")
    return is_show_stats

#изменение интервала повторения
def get_new_interval(word: str) -> None:
    interval = stats[word][INTERVAL]
    status = stats[word][STATUS]
    max_index = len(STATUSES[stats[word][STATUS]][INTERVALS]) - 1
    min_interval = STATUSES[stats[word][STATUS]][INTERVALS][0]
    current_index = STATUSES[status][INTERVALS].index(interval)
    if  stats[word][STREAK] >= TRANSITION_INTERVAL_THRESHOLD_UP:
        stats[word][INTERVAL] = STATUSES[status][INTERVALS][min(current_index + 1, max_index)]
    elif stats[word]["incorrect_per_session"] >= TRANSITION_INTERVAL_THRESHOLD_DOWN:
        stats[word][INTERVAL] = STATUSES[status][INTERVALS][min(current_index - 1, 0)]

#установка следующей даты повторения
def set_next_show(word: str) -> None:
    interval = stats[word][INTERVAL]
    stats[word][NEXT_SHOW]  = date.today() + timedelta(days=interval)
#установка параметров сессии пользователем
def set_session_params() -> int:
    
#установка количества слов
    prompt = f"Введите количество слов для изучения (5-20) или нажмите Enter, чтобы оставить по умолчанию {DEFAULT_COUNT_WORDS}: "
    count_words = input_number(prompt, MIN_COUNTS_WORDS, MAX_COUNTS_WORDS, DEFAULT_COUNT_WORDS)
    if count_words is None:
        print("Ввод отменен.")
        count_words = DEFAULT_COUNT_WORDS
            
#установка максимального количества циклов
    return count_words

#сохранение копии словаря
def save_start_stats(should_save: bool) -> None:
    if should_save:
        start_stats.clear()
        start_stats.update(deepcopy(stats))
    else:
        stats.clear()
        stats.update(start_stats)

#вывод статистики по сессии
def prepare_stats_for_display(count_words: int, session_stats: dict, session_list: list) -> None:
    session_words_stats = []
    
    headers = [["English word/", "Перевод"], ["Всего", "показов"], ["Верных/", "неверных", "ответов"], ["Верных", "ответов", "подряд"], ["Интервал"], ["Срок", "показа"], ["Статус", "до сессии"], ["Статус", "после", "сессии"]]
    total_shows = session_stats["shows"]
    total_correct =session_stats["correct"]
    total_incorrect = total_shows - total_correct
    accuracy = round(total_correct/total_shows, 2)

    total_session_stats = [("Всего показано слов:", str(count_words)), ("Всего ответов:", str(total_shows)), ("Всего правильных ответов:", str(total_correct)), ("Всего неправильных ответов:", str(total_incorrect)), ("Общая точность ответов:", str(accuracy) + "%")]
    show_table(title="Общая статистика прогресса обучения за сессию", data=total_session_stats)

    for word in session_list:
        shows = stats[word][SHOWS] - start_stats[word][SHOWS]
        correct = stats[word][CORRECT] - start_stats[word][CORRECT]
        incorrect = shows - correct
        streak = stats[word][STREAK]
        interval = stats[word][INTERVAL]
        next_show = stats[word][NEXT_SHOW]
        old_status = start_stats[word][STATUS]
        new_status = stats[word][STATUS]
    
        line = ([word, vocabulary[word][TRANSLATION]], str(shows), str(correct) + "/" + str(incorrect), str(streak), str(interval), next_show.strftime("%d.%m.%y"), old_status, new_status)
        session_words_stats.append(line)

    show_table("Прогресс по результатам сессии", session_words_stats, headers)
#функция запуска режима тренировки
def start_session() -> None:
    clear_screen()
    session_stats = {
    "shows": 0,
    "correct": 0,
}
    #сохраняем копию словаря до начала тренировки
    save_start_stats(should_save=True)
    count_words = set_session_params()
    calculate_priority()
    session_list, count_words = get_learning_words(count_words)
    
    if not session_list:
        print("Нет слов для изучения.")
        return

    set_counts_cycles(session_list)
    is_show_stats = training_session(session_list, session_stats)
    if  is_show_stats:
        for word in session_list:
            get_new_interval(word)
            set_new_status(word)
            set_next_show(word)
        prepare_stats_for_display(count_words, session_stats, session_list)
    pause()