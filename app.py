"""
Задание 1:
В папке files/ лежит файл с каталогом продукции (стекло лобовое, заднее, боковое и различные аксессуары: клей, молдинги)
Нужно считать информацию из этого каталога и записать в файл json. Нужные листы в каталоге
["Автостекло. Аксессуары. Клей", "Российский автопром"]
Автостекло. Аксессуары. Клей - это каталог "Иномарки"
Российский автопром - это каталог "Отечественные"
Нужные столбцы ["Вид стекла", "Еврокод", "Код AGC", "Старый Код AGC", "Наименование", "ОПТ"]
Обратить внимание - Если у позиции цена фиксированная, то в столбце ОПТ будет *, поэтому такие случаи нужно учесть и в
цену ставить Фиксированную цену.
Структура объекта в json-файле:
    {
        "art": Код AGC,
        "eurocode": Еврокод,
        "oldcode": Старый Код AGC,
        "name": Наименование,
        "catalog": Иномарки или отечественные (смотря из какой вкладки каталога позиция)
        "category": Вид стекла,
        "price": Цена ОПТ или Фиксированная
    }
"""
import json

import pandas as pd
import numpy as np

url_file = "https://github.com/Pahteev/test_task1/raw/main/files/%D0%9F%D1%80%D0%B0%D0%B9%D1%81-%D0%BB%D0%B8%D1%81%D1%82%20AGC%202024.03.04%20%D0%9E%D0%BF%D1%82.xlsx"
url_local = r"C:\Users\Admin\Desktop\Study\Гласс рус задание\Прайс-лист AGC 2024.03.04 Опт.xlsx"

sales = pd.read_excel(
    url_local,
    engine="openpyxl",
    sheet_name=['Автостекло. Аксессуары. Клей', "Российский автопром"],
    header=4,
)
list_json = [] # список, в который записываем словари для JSON

'''Получаем все иномомарки из файла, и удаляем пустые строки'''
foreign_car = sales['Автостекло. Аксессуары. Клей']  # получаем таблицу иномарок
foreign_car_supp = foreign_car[["Вид стекла", "Еврокод", "Код AGC", "Наименование", "Цена фиксирована",
                                "ОПТ"]]  # фильтруем иномарки по нужным столбцам, вспомогательная переменная
foreign_car_clear = foreign_car_supp[foreign_car_supp[
    "Код AGC"].notna()]  # фильтруем таблицу иномарок, убирая пустые строки ориентируясь на столбец "Код AGC"

'''Получаем все отечественные из файла, и удаляем пустые строки'''
rus_car = sales['Российский автопром']  # получаем таблицу отечественных
rus_car_supp = rus_car[["Вид стекла", "Код AGC", "Старый Код AGC", "Наименование", "Цена фиксирована",
                        "ОПТ"]]  # фильтруем отечетвенные по нужным столбцам, вспомогательная переменная
rus_car_clear = rus_car_supp[rus_car_supp[
    "Код AGC"].notna()]  # фильтруем таблицу отечественных, убирая пустые строки ориентируясь на столбец "Код AGC"


def create_json(data):
    for i in range(len(data)):
        dict_element = {}
        dict_element["art"] = int(data.iloc[i]["Код AGC"])
        dict_element["name"] = data.iloc[i]["Наименование"]
        if "Еврокод" in data:
            dict_element["eurocode"] = data.iloc[i]["Еврокод"]
            dict_element["catalog"] = 'Автостекло. Аксессуары. Клей'
            dict_element["price"] = data.iloc[i]['ОПТ']
        else:
            dict_element["catalog"] = 'Российский автопром'
        if str(data.iloc[i]['ОПТ']) == '*':
            dict_element["price"] = float(data.iloc[i]['Цена фиксирована'])
        else:
            dict_element["price"] = data.iloc[i]['ОПТ']
        dict_element["category"] = data.iloc[i]['Вид стекла']
        list_json.append(dict_element)
    return list_json


# create_json(foreign_car_clear)
# print(create_json(rus_car_clear))

'''Записываем полученный писок словарей в JSON  - файл'''
# with open("data_file.json", "w", encoding='utf-8') as write_file:
#     json.dump(list_json, write_file, ensure_ascii=False, )
"""

Задание 2:
Опираясь на полученную информацию сформировать катлог для клиента. Для клиента нужны только товары из категорий
["ветровое", "заднее", "боковое"]
Цены для клиента рассчитываются по следующему принципу:
ветровое - (цена price из каталога + 1000) + 5%
заднее - (цена price из каталога + 800) + 7%
боковое - цена price из каталога + 10%
В итоге должны получить excel-файл с расшиернием .xlsx
-----------------------------------------------------------------------
| catalog | category | art | eurocode | oldcode | name | client_price |
-----------------------------------------------------------------------
"""

f = open(r"C:\Users\Admin\Desktop\Study\Гласс рус задание\data_file.json")
json_local = json.loads(f)
f.close()
print(json_local)