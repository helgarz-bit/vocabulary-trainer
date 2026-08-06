from storage import load, save_json, vocabulary, stats
from menu import menu

def main():
#загрузка данных
    load(vocabulary, "dictionary.json")
    load(stats, "statistics.json")

    menu()

    #сохранение словарей в файл
    save_json(vocabulary, "dictionary.json")
    save_json(stats, "statistics.json")

main()