import shutil

from storage import vocabulary, stats
from config import *

SCREEN_WIDTH= shutil.get_terminal_size().columns

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


#подготовка данных к печати
def prepare_data_to_print(data: list|dict, word: str|None =None) -> list:
    output_data = []
    if isinstance(data, dict):
        if data == vocabulary:
            field_voc = FIELDS
        elif data == stats:
            field_voc = stats_fields
        if word is not None:
            for field_name, field_data in field_voc.items():
                if field_name == WORD:
                    output_data.append(([field_data[PROMPT]], [word]))
                    continue
                characteristic =  data[word]
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
def calculat_width_column( rows: list, headers: list|None) -> list:
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
    
    width_column.append(width_table)
    
    return width_column

#вывод таблицы на экран
def display_table(rows: list, width_column: list, headers: list|None) -> None:
    column_count = len(rows[0])
    width_table = width_column.pop()
    
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
    if isinstance(data, tuple):
        dictionary, word = data
        rows = prepare_data_to_print(dictionary, word)
    else:
        rows = prepare_data_to_print(data)
    
    
    width_columns = calculat_width_column(rows, headers)
    width_table = width_columns[-1]
    
    print(title.upper().center(width_table))
    display_table(rows, width_columns, headers)
    

#про    верка работы модуля
#total_session_stats = [("Всего показано слов:", str(23)), ("Всего ответов:", str(12)), ("Всего правильных ответов:", str(12)), ("Всего неправильных ответов:", str(4)), ("Общая точность ответов:", str(4) + "%")]

#print(prepare_data_to_print(total_session_stats))