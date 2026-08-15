from storage import load, load_json, save_json, vocabulary, stats, categories, convert_date_to_string, convert_string_to_date, prepare_dict_for_save
from menu import menu
from config import DEFAULT_CATEGORY, NEXT_SHOW
import utils

def main():
#загрузка данных
    load(vocabulary, "dictionary.json")
    load(stats, "statistics.json")
    convert_string_to_date(stats, NEXT_SHOW)
    
    categories[:] = load_json("categories.json", [])

    if not categories:
        categories.append(DEFAULT_CATEGORY)

    menu()

#подготовка словаря  к сохранению
    stats_for_safe = prepare_dict_for_save(stats)
    convert_date_to_string(stats_for_safe, NEXT_SHOW)
    save_json(vocabulary, "dictionary.json")
    save_json(stats_for_safe, "statistics.json")
    save_json(categories, "categories.json")

main()