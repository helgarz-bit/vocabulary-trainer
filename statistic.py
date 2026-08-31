from datetime import date

from utils import answer_dialog, clear_screen, what_to_do, pause
from storage import vocabulary, stats
from dictionary import get_word_key
from display import show_table
from config import  (
    SHOWS,
    CORRECT,
    STREAK,
    INTERVAL,
    NEXT_SHOW,
    LAST_WRONG,
    STATUS,
    TRANSLATION,
    DIFFICULT_THRESHOLD,
    NEW,
    LEARNING,
    CONSOLIDATING,
    REVIEWING,
    STATUSES,
    INTERVALS

)
    
MIN_SHOWS_FOR_STATS = 5

#общая статистика
def show_total_stats() -> None:
    new_words = 0
    learning_words = 0
    consolidating_words = 0
    reviewing_words = 0
    shows = 0
    correct = 0
    showed_words = 0
    max_streak = 0
    total_streak = 0
    overdue_words = 0
    total_words =     len(vocabulary)
    today = date.today()
    for values in stats.values():
        shows += values[SHOWS]
        correct += values[CORRECT]
        if values[STATUS] == NEW:
            new_words += 1
        elif values[STATUS]     == LEARNING:
            learning_words += 1
        elif values[STATUS] == CONSOLIDATING:
            consolidating_words += 1
        elif values[STATUS] == REVIEWING:
            reviewing_words += 1

        total_streak += values[STREAK]
        if values[SHOWS] > 0:
            showed_words += 1
        
        if values[STREAK] > max_streak:
            max_streak = values[STREAK]

        if (values[NEXT_SHOW] is not None) and (values[NEXT_SHOW] < today):
            overdue_words += 1

    if shows == 0:
        accuracy      = 0
    else:    
        accuracy = round(correct / shows * 100, 2) 
    incorrect = shows - correct
    mean_streak = round(total_streak / showed_words , 2)
    total_stats = [
    ("Всего слов в словаре", str(total_words)),
    ("новых слов", str(new_words)),
     ("изучаются", str(learning_words)),
     ("закрепляются", str(consolidating_words)),
      ("повторяются", str(reviewing_words)),
      ("Всего показано слов ", str(showed_words)),
      ("дано ответов", str(shows)),
       ("верных ответов", str(correct)),
       ("неверных ответов", str(incorrect)),
       ("точность ответов", str(accuracy)),
       ("максимальная серия верных ответов", str(max_streak)),
       ("средняя серия верных ответов", str(mean_streak)),
       ("слов с просроченным сроком повторения", str(overdue_words))
]
    show_table(title="Общая статистика", data=total_stats)


#вывод списка самых трудных слов
def show_difficult_words() -> None:
    title = 'Список "трудных" слов'
    rows = []
    headers = [["Слово"], ["Точность ответов"], ["Верных ответов"], ["Всего ответов"]]

#слова с достаточным количеством показов и низкой точностью ответов
    difficult_list = [(word, values[CORRECT], values[SHOWS]) for word, values in stats.items() if values[SHOWS] >= MIN_SHOWS_FOR_STATS and values[CORRECT] / values[SHOWS] < DIFFICULT_THRESHOLD]
        
    if difficult_list:
        difficult_list.sort(key=lambda item: item[1])
        for element in difficult_list:
            row = (element[0], f"{element[1] / element[2] * 100:.2f} %", str(element[1]), str(element[2]))
            rows.append(row)

        show_table(title=title, data=rows, headers=headers)
    else:
        print("Трудных слов не найдено.")

        #статистика по результатам сессии
def show_session_results(start_stats: dict, session_list: list) -> None:
    session_words_stats = []
    
    headers = [["English word/", "Перевод"], ["Всего", "показов"], ["Верных/", "неверных", "ответов"], ["Верных", "ответов", "подряд"], ["Интервал"], ["Срок", "показа"], ["Статус", "до сессии"], ["Статус", "после", "сессии"]]
    total_shows = sum(stats[word][SHOWS]  - start_stats[word][SHOWS] for word in session_list) 
    total_correct =sum(stats[word][CORRECT] - start_stats[word][CORRECT] for word in session_list) 
    total_incorrect = total_shows - total_correct
    accuracy = round(total_correct / total_shows  * 100, 2)
    count_words = len(session_list)

    total_session_stats = [("Всего показано слов:", str(count_words)), ("Всего ответов:", str(total_shows)), ("Всего правильных ответов:", str(total_correct)), ("Всего неправильных ответов:", str(total_incorrect)), ("Общая точность ответов:", str(accuracy) + "%")]
    show_table(title="Общая статистика результатов сессии", data=total_session_stats)

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

    show_table("Прогресс изучения по словам", session_words_stats, headers)


def show_word_stats() -> None:
    print("Вывод статистики по выбранному слову.\nq - отмена")
    
    word =  get_word_key(must_be=True,  )

    if word is None:
        print("Вывод статистики отменен")
        return

    if word  not in stats:
        print(f"Статистика по слову {word} не найдено.")
        return 

    show_table(title=f"статистика изучения слова {word}", data=(stats, word))

#обнуление статистики
def reset_stats() -> None:
    if answer_dialog("Вы действительно хотите обнулить статистику?"):
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
          
#сводная таблица по статистике слов
def show_summary_stats() -> None:
    rows = []
    title = "Сводная таблица статистики изучения слов"
    headers = [["Слово"], ["Перевод"], ["Всего", "показов"], ["Верных", "ответов"], ["Неверных ", "ответов"], ["Серия", "верных", "ответов"], ["Интервал", "повторения"], ["Срок", "повторения"], ["Статус"]]

    for word, values in stats.items():
        shows = values[SHOWS]
        correct = values[CORRECT]
        incorrect = shows - correct
        streak = values[STREAK]
        interval = values[INTERVAL]
        if values[NEXT_SHOW]:
            next_show = values[NEXT_SHOW].strftime("%d.%m.%y")
        else:
            next_show = "-"
        status = values[STATUS]
        row = (word, vocabulary[word][TRANSLATION], str(shows), str(correct), str(incorrect), str(streak), str(interval), next_show, status)
        rows.append(row)
    show_table(title=title, data=rows, headers=headers)
#менеджер функций
def manager_stats(action: str)    :
    clear_screen()
    if not stats:
        print("Данные статистики отсутствуют. Вывод данных невозможен.")
        pause()
        return
    repeat = False
    while True:
        match action:
            case "total":
                show_total_stats()
            case "stats_word":
                show_word_stats()
                repeat = True
            case "difficult":
                show_difficult_words()
            case "summary":
                show_summary_stats()
            case "reset":
                reset_stats()
            case "return":
                break

        action = what_to_do(repeat=repeat, action=action)
        
