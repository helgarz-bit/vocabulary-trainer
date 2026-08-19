import os
import shutil
from datetime import date

from config import  *
from utils import input_dialog, answer_dialog, clear_screen, what_to_do
from storage import vocabulary, stats
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

        total_streak = values[STREAK]
        if values[SHOWS] > 0:
            showed_words += 1

        #if values[STREAK] < MIN_STREAK:
            #min_streak = values[STREAK]
        #if values[STREAK] > max_streak:
         #   max_streak = values[STREAK]

            if values[NEXT_SHOW] < date.today():
                overdue_words += 1
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

def stats_word() -> None:
    print("Вывод статистики по выбранному слову. Для отмены введите 'q'")
    
    word = input_dialog("Введите слово для отображения по нему статистики: ", FIELDS[WORD][SETTINGS])

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


#разбиение длинного слова на части фиксированной длины
def split_long_word(word: str, width: int) -> list:
    parts_word = []
    i = 0
    while i < len(word):
        part = word[i:i+width-1]
        if i + width < len(word):
            part += "-"

        parts_word.append(part)
        i += width - 1
    return parts_word


#разбиение длинной строки на строки фиксированной длины
def split_into_lines(text: str, width: int)-> list:
    lines = []
    current_line = []     
    words = text.split()
    for word in words:
        current_line.append(word) 
        if len(" ".join(current_line)) > width:
             current_line.pop()
             lines.append(" ".join(current_line))
             current_line.clear()
             current_line.append(word)

    if current_line:
         lines.append(" ".join(current_line))
    return lines

            
          
#менеджер функций
def manager_stats(action: str)    :
    clear_screen()
    repeat = False
    while True:
        match action:
            case "total":
                total_stats()
            case "stats_word":
                stats_word()
                repeat = True
            case "dificault":
                stats_difficult_words()
            case "rewrite":
                set_default()
            case "return":
                break

        do = what_to_do(repeat=repeat)
        if do != 'r':
            action = do
    
