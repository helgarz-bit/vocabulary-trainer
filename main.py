from storage import load, load_json, save_json, vocabulary, stats, categories
from menu import menu
from config import DEFAULT_CATEGORY
import utils

def main():
#загрузка данных
    load(vocabulary, "dictionary.json")
    load(stats, "statistics.json")
    categories[:] = load_json("categories.json", [])
    
    if not categories:
        categories.append(DEFAULT_CATEGORY)
    
    menu()

    #сохранение данных в файл
    save_json(vocabulary, "dictionary.json")
    save_json(stats, "statistics.json")
    save_json(categories, "categories.json")

main()