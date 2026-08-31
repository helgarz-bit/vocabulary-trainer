import shutil

from storage import vocabulary, stats
from config import *
from utils import pause

#подготовка данных к печати
def prepare_data_to_print(data: list|dict, word: str|None =None) -> list:
    """Подготавливает данные к выводу в табличном формате.
    Функция преобразует словарь или список данных в единый формат,
    используемый функциями вывода таблиц.
    Если data является словарем vocabulary или stats и 
    указан параметр word, формируется список данных для одного слова.
    Если word не указан, формируется список для всех записей словаря.
    Если data является списком, то каждый элемент преобразуется в структуру, в которой отдельные значения представлены списками.
    
    Args:
        data: Словарь или список данных, предназначенные для вывода.
        word: Слово, для которого необходимо подготовить данные.
        Если значение не указано, подготавливаются данные для всех записей словаря.
        
    Returns:
        Список подготовленных данных, пригодных для формирования и вывода таблицы.
    """
    output_data = []
    if isinstance(data, dict):
        if data == vocabulary:
            field_voc = FIELDS
        elif data == stats:
            field_voc = stats_fields
        if word is not None:
            characteristic =  data[word]
            for field_name, field_data in field_voc.items():
                if field_name == WORD:
                    output_data.append(([field_data[PROMPT]], [word]))
                    continue
                
                if data == vocabulary:
                    output_data.append(([field_data[PROMPT]], [characteristic[field_name]]))
                else:
                    if not isinstance(characteristic[field_name], str):
                        value = str(characteristic[field_name])
                    else:
                        value = characteristic[field_name]
                    output_data.append(([field_data], [value]))
        else:
            for word, values in data.items():
                element = []
                element.append([word])
                for value in values.values():
                    element.append([value])
                output_data.append(tuple(element))

    else:
        for note in data:
            element_data = []
            for  element in note:
                if isinstance(element, list):
                    element_data.append(element)
                else:
                    element_data.append([element])
            output_data.append(tuple(element_data))

    return output_data

#расчет ширины столбцов таблицы
def calculate_width_column( rows: list, headers: list|None) -> tuple:
    width_column = []
    column_count = len(rows[0])
    spaces = 2
    separators = column_count - 1

    for col in range(column_count):
        if headers:
            width_header = max(len(line) for line in headers[col])
        else:
            width_header = 0

        width_data = max(len(line) for row in rows for line in row[col])
        width_col  = max(width_header, width_data) + spaces
        width_column.append(width_col)

    width_table = sum(width_column) + separators
    
    return (width_column, width_table)

#вывод таблицы на экран
def display_table(rows: list, width_params: tuple, headers: list|None) -> None:
    """Выводит данные в виде таблицы в консоль.
    
    Поддерживает многострочные значения в ячейках. Если значение 
    ячейки занимает меньше максимального числа строк, недостающие строки заполняются пробелами.
    При наличии перед данными выводятся заголовки столбцов.
    
    Args:
        rows: Строки таблицы. Каждая строка содержит 
        список ячеек, а содержимое каждой ячейки представлено списком строк.
        width_params: Кортеж из двух элементов: списка ширины столбцов
        и общей ширины таблицы.
        headers: Заголовки столбцов, представленные в том же формате,что и данные.
        Если значение None, то заголовки не выводятся.
    """
    column_count = len(rows[0])
    width_column,  width_table = width_params
    
    print("_" * width_table)

    if headers:
        max_lines_header = max(len(lines) for lines in headers)
    
        for line in range(max_lines_header):        
            cells = []
            for col in range(column_count):
                
                if line < len(headers[col]):
                    value = headers[col][line]
                else:
                    value = " "
            
                cells.append(f" {value:<{width_column[col]}}")

            header_line = "|".join(cells)
            print(header_line)
        print("_" * width_table)

    max_lines_rows = max(len(col) for row in rows for col in row)
    for row in rows:
        for line in range(max_lines_rows):
            cells = []
            for col in range(column_count):
                if line < len(row[col]):
                    value = row[col][line]
                else:
                    value = " "

                cells. append(f" {value:<{width_column[col]}}")
            row_line = "|".join(cells)
            print(row_line)
        print("_" * width_table)

#вывод таблицы на экран
def show_table(title: str, data: list|tuple, headers: list|None =None) -> None:
    """Подготавливает данные и выводит в виде таблицы.
    
    Проверяет наличие данных, подготавливает их для вывода,
    расчитывает ширину столбцов и выводит таблицу с указанным заголовком.
    
    Если data является кортежем, он должен содержатьсловарь и слово.
    В этом случае выводятся данные только для указанного слова.
    Если data является списком, то выводятся все содержащиеся в нем данные.
    
    Args:
        title: Заголовок таблицы.
        data: Данные для вывода. Может содержать список данных или
        кортеж из словаря и слова для вывода данных конкретного слова.
        headers: Заголовки столбцов. Если значение None, то 
        заголовки не выводятся.
    """
    if isinstance(data, tuple):
        dictionary, word = data
        if dictionary:
            rows = prepare_data_to_print(dictionary, word)
        else:
            print("Словарь пуст. Вывод данных невозможен.")
            pause()
            return
    else:
        if data:
                rows = prepare_data_to_print(data)
        else:
            print("Данные отсутствуют. Вывод данных невозможен.")
            pause()
            return
    
    width_params = calculate_width_column(rows, headers)
    width_columns, width_table = width_params
    print(title.upper().center(width_table))
    display_table(rows, width_params, headers)
    

#про    верка работы модуля
#total_session_stats = [("Всего показано слов:", str(23)), ("Всего ответов:", str(12)), ("Всего правильных ответов:", str(12)), ("Всего неправильных ответов:", str(4)), ("Общая точность ответов:", str(4) + "%")]

#print(prepare_data_to_print(total_session_stats))