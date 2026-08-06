import random

from config import (STATUS, NOT_LEARNED, LEARNED,
                       TRANSLATION, SHOWS, STREAK, CORRECT, STREAK_THREE)
from storage import  vocabulary, stats
from utils import  input_dialog, answer_dialog, clear_screen, pause

DEFAULT_COUNT_WORDS = 5
DEFAULT_CYCLES = 5
STREAK_TO_REMOVE = 3
STREAK_TO_LEARNED = 5

TRAINER_SETTINGS = {
    "validation": True,
    "required": True,
    "to_lower": True
}


#получение списка слов на сессию
def get_learning_words(count_words: int) -> tuple:
#формируем список из неизученных слов
    learning_words = [word for word in vocabulary.keys() if stats[word][STATUS] == NOT_LEARNED]
    count_words = min(len(learning_words), count_words)
    
    #выбираем из списка слова на текущую сессию случайным образом
    list_for_learn = random.sample(learning_words, count_words)
    return (list_for_learn, count_words)

#функция показа слова из списка
def training_session(learning_list: list, session_stats: dict) -> bool|None:
    is_show_stats = True
    print("Начало сессии режима обучения.")
    
    for  count in range(DEFAULT_CYCLES):
        random.shuffle(learning_list)
        count_words =  len(learning_list)
        for _ in range(count_words):
            word = learning_list.pop(0)
            translation = vocabulary[word][TRANSLATION]
            
            stats[word][SHOWS] += 1 #увел ичиваем счетчик показов слова
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
                
            streak = stats[word][STREAK] 
            if streak == STREAK_TO_REMOVE:
                session_stats[STREAK_THREE] +=1
            elif streak == STREAK_TO_LEARNED:
                stats[word][STREAK] +=1
                stats[word][STATUS] = LEARNED
                session_stats[LEARNED] +=1
            else:
                learning_list.append(word)
                

    print("Сессия закончена.")
    return is_show_stats

#установка параметров сессии пользователем
def set_session_params() -> int:
    count_words = input(f"Введите количество слов для изучения или нажмите Enter, чтобы оставить по умолчанию {DEFAULT_COUNT_WORDS}: ").strip()
    if not count_words:
        count_words = DEFAULT_COUNT_WORDS
    #count_repeat = int(input("Введите максимальное число повторений: ").strip())
    return int(count_words)
#вывод статистики по сессии
def show_session_stats(count_words: int, session_stats: dict) -> None:
    print("Статистика прогресса за сессию")
    print(f"Всего показано {count_words} слов {session_stats[SHOWS]} раз")
    print(f"верных ответов: {session_stats[CORRECT]}")
    print(f"Неверных ответов: {session_stats[SHOWS]-session_stats[CORRECT]}")
    print(f"Слов с тремя верными ответами подряд: {session_stats[STREAK_THREE]}")
    print(f"За сессию выучено  {session_stats[LEARNED]} слов")

#функция запуска режима тренировки
def start_session() -> None:
    clear_screen()
    session_stats = {
    "shows": 0,
    "correct": 0,
    "learned": 0,
    "streak_three": 0
}

    count_words = set_session_params()
    learning_list, count_words = get_learning_words(count_words)

    if not learning_list :
        print("Нет слов для изучения.")
        return

    is_show_stats = training_session(learning_list, session_stats)
    if is_show_stats:
        show_session_stats(count_words, session_stats)
        pause()