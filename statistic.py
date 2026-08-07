from config import  *
from utils import input_dialog, answer_dialog, clear_screen, what_to_do
from storage import vocabulary, stats

DIFFICULT_THRESHOLD = 0.6
MIN_SHOWS_FOR_STATS = 5

#общая статистика
def total_stats() -> None:
    total_words =     len(vocabulary)
    learned_words = sum(1 for value in stats.values() if  value[STATUS] == LEARNED)
    not_learned_words = sum(1 for value in stats.values() if value[STATUS] == NOT_LEARNED)
    procent_learn = round(learned_words/total_words*100, 2)
    strek_0 = sum(1 for value in stats.values() if value["streak"] == 0)
    strek_1 = sum(1 for value in stats.values() if value[STREAK] == 1)
    strek_2 = sum(1 for value in stats.values() if value[STREAK] == 2)
    strek_3 = sum(1 for value in stats.values() if value[STREAK] == 3)
    strek_4 = sum(1 for value in stats.values() if value[STREAK] == 4)

    print(f"Всего слов в словаре: {total_words}")
    print(f"Выучено {learned_words} слов.")
    print(f"Невыученных слов: {not_learned_words}")
    print(f"Словарь выучен на {procent_learn}%")
    print(f"Выучено на 0%: {strek_0}")
    print(f"Выучено на 20%: {strek_1}")
    print(f"Выучено на 40%: {strek_2}")
    print(f"Выучено на 60%: {strek_3}")
    print(f"Выучено на 80%: {strek_4}")

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
    
    show_stats_word(word)

#обнуление статистики
def set_default() -> None:
    answer = answer_dialog("Вы действительно хотите обнулить статистику?")  
    if answer:
        for  value in stats.values():
            value[SHOWS] = 0
            value[CORRECT] = 0
            value[STREAK] = 0
            value[STATUS] = NOT_LEARNED
        print("Статистика успешно обнулена.")
    else:
        print("Обнуление статистики отменено.")
            
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
    
