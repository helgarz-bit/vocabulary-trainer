import os
import shutil
from datetime import date

from config import  *
from utils import input_dialog, answer_dialog, clear_screen, what_to_do
from storage import vocabulary, stats
from dictionary import get_word_key
from display import show_table
DIFFICULT_THRESHOLD = 0.6
MIN_SHOWS_FOR_STATS = 5

#общая статистика
def total_stats() -> None:
    new_words = 0
    learning_words = 0
    consolidating_words = 0
    reviewing_words = 0
    shows = 0
    correct = 0
    showed_words = 0
    min_streak = 0
    max_streak = 0
    total_streak = 0
    overdue_words = 0
    total_words =     len(vocabulary)
    for values in stats.values():
        shows += values[SHOWS]
        correct += values[CORRECT]
        if values[STATUS] == "new":
            new_words += 1
        elif values[STATUS]     == "learning":
            learning_words += 1
        elif values[STATUS] == "consolidating":
            consolidating_words += 1
        elif values[STATUS] == "reviewing":
            reviewing_words += 1

        total_streak += values[STREAK]
        if values[SHOWS] > 0:
            showed_words += 1
        
        if values[STREAK] > max_streak:
            max_streak = values[STREAK]

        if (values[NEXT_SHOW] is not None) and (values[NEXT_SHOW] < date.today()):
            overdue_words += 1

    if shows == 0:
        print("Статистика по словам отсутствует. Вывод данных невозможен.")
        return
    accuaracy = round(correct / shows * 100, 2) 
    incorrect = shows - correct
    mean_streak = round(total_streak / showed_words , 2)
    total_stats = [
    ("Всего слов в словаре", str(total_words)),
    ("новых слов", str(new_words)),
     ("изучаются", str(learning_words)),
     ("закрепляются", str(consolidating_words)),
      ("повторяются", str(reviewing_words)),
      ("Всего показано слов", str(showed_words)),
      ("дано ответов", str(shows)),
       ("верных ответов", str(correct)),
       ("неверных ответов", str(incorrect)),
       ("точность ответов", str(accuaracy)),
       ("максимальная серия верных ответов", str(max_streak)),
       ("средняя серия верных ответов", str(mean_streak)),
       ("слов с просроченным сроком повторения", str(overdue_words))
]
    show_table(title="Общая статистика", data=total_stats)


#вывод списка самых трудных слов
def stats_difficult_words():
    print('Список "трудных" слов')
    show_words_list = [(word, values[CORRECT], values[SHOWS]) for word, values in stats.items() if values[SHOWS] > 0]
    difficult_list = [item for item in show_words_list if item[1]/item[2] < DIFFICULT_THRESHOLD and item[2] >= MIN_SHOWS_FOR_STATS]
        
    if difficult_list:
        difficult_list.sort(key=lambda item: item[1]/item[2])
        for word, correct, shows in difficult_list:
                print(f"{word} - {correct/shows * 100:.2f}% {correct} из {shows} верных ответов")
    else:
        print("Трудных слов не найдено.")

        #вывод статистики по отдельному слову
def show_stats_word(word: str) -> None:
    print(f"Статистика изучения слова {word}")
    for param_key, prompt in stats_fields.items():
            print(f"{prompt}:  {stats[word][param_key]}")
#статистика по результатам сессии
def stats_session_results(start_stats: dict, session_list: list) -> None:
    session_words_stats = []
    
    headers = [["English word/", "Перевод"], ["Всего", "показов"], ["Верных/", "неверных", "ответов"], ["Верных", "ответов", "подряд"], ["Интервал"], ["Срок", "показа"], ["Статус", "до сессии"], ["Статус", "после", "сессии"]]
    total_shows = sum(stats[word][SHOWS]  - start_stats[word][SHOWS] for word in session_list) 
    total_correct =sum(stats[word][CORRECT] - start_stats[word][CORRECT] for word in session_list) 
    total_incorrect = total_shows - total_correct
    accuracy = round(total_correct / total_shows  * 100, 2)
    count_words = len(session_list)

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


def stats_word() -> None:
    print("Вывод статистики по выбранному слову. Для отмены введите 'q'")
    
    word =  get_word_key(must_be=True,  )

    if word is None:
        print("Вывод статистики отменен")
        return

    if word  not in stats:
         print(f"Статистика по слову {word} не найдено.")
    
    show_table(title=f"статистика изучения слова {word}", data=(stats, word))

#обнуление статистики
def set_default() -> None:
    answer = answer_dialog("Вы действительно хотите обнулить статистику?")  
    if answer:
        for  word, value in stats.items():
            value[SHOWS] = 0
            value[CORRECT] = 0
            value[STREAK] = 0
            value[STATUS] = NEW
            value[LAST_WRONG] = 0
            value[NEXT_SHOW] = None
            value[INTERVAL] = STATUSES[NEW][INTERVALS][0]
        print("Статистика успешно обнулена.")
    else:
        print("Обнуление статистики отменено.")
          
#менеджер функций
def manager_stats(action: str)    :
    clear_screen()
    if not stats:
        print("Данные статистики отсутствуют. Вывод данных невозможен.")
        input("Нажмите Enter для возврата в меню")
        return
    repeat = False
    while True:
        match action:
            case "total":
                total_stats()
            case "stats_word":
                stats_word()
                repeat = True
            case "difficult":
                stats_difficult_words()
            case "rewrite":
                set_default()
            case "return":
                break

        do = what_to_do(repeat=repeat)
        if do != 'r':
            action = do
    
