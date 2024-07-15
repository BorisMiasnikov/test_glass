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
import pprint

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

foreign_car = sales['Автостекло. Аксессуары. Клей']  # получаем таблицу иномарок
def create_json(data): #в дату теперь передаем весь датафрейм
    list_json = []
    for list in data.keys():
        foreign_car = data[list]
        foreign_car_supp = foreign_car[["Вид стекла", "Еврокод", "Код AGC", "Старый Код AGC", "Наименование", "Цена фиксирована", "ОПТ"]]
        foreign_car_clear = foreign_car_supp[foreign_car_supp["Код AGC"].notna()]
        for i in range(len(foreign_car_clear)):
            dict_element = {}
            dict_element["art"] = int(foreign_car_clear.iloc[i]["Код AGC"])
            dict_element["oldcode"] = foreign_car_clear.iloc[i]["Старый Код AGC"]
            dict_element["name"] = foreign_car_clear.iloc[i]["Наименование"]
            dict_element["eurocode"] = foreign_car_clear.iloc[i]["Еврокод"]
            dict_element["catalog"] = list
            if str(foreign_car_clear.iloc[i]['ОПТ']) == '*':
                dict_element["price"] = float(foreign_car_clear.iloc[i]['Цена фиксирована'])
            else:
                dict_element["price"] = foreign_car_clear.iloc[i]['ОПТ']
            dict_element["category"] = foreign_car_clear.iloc[i]['Вид стекла']
            list_json.append(dict_element)
    return list_json


'''Записываем полученный список словарей в JSON  - файл'''
with open("data_file.json", "w", encoding='utf-8') as write_file:
    json.dump(create_json(sales), write_file, ensure_ascii=False, indent=4)
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

# # with open('data_file.json', 'r', encoding='utf-8') as json_file:
# #     json_local = json.load(json_file)
# #
# # detail_data = []
# # detail_columns = []
#
# def client_price(data):
#     if data['category'] == "ветровое":
#         price = (float(data['price'])+1000)+(float(data['price'])+1000)*0.05
#         return price
#     elif data['category'] == "заднее":
#         price = (float(data['price'])+800)+(float(data['price'])+800)*0.07
#         return price
#     elif data['category'] == "боковое":
#         price = float(data['price'])+float(data['price'])*0.1
#         return price
#
#
# for i in json_local:
#     if i['category'] == "ветровое" or "заднее" or "боковое":
#         detail_data_unit = []
#         if "eurocode" in i.keys():
#             detail_data_unit.append(i['catalog'])
#             detail_data_unit.append(i['category'])
#             detail_data_unit.append(i['art'])
#             detail_data_unit.append(i['eurocode'])
#             detail_data_unit.append('0')
#             detail_data_unit.append(i['name'])
#             detail_data_unit.append(client_price(i))
#         else:
#             detail_data_unit.append(i['catalog'])
#             detail_data_unit.append(i['category'])
#             detail_data_unit.append(i['art'])
#             detail_data_unit.append(0)
#             detail_data_unit.append(i['oldcode'])
#             detail_data_unit.append(i['name'])
#             detail_data_unit.append(client_price(i))
#         detail_data.append(detail_data_unit)
#
#
# print(detail_data)
''' для записи экселя
df1 = pd.DataFrame([[первая строка], [вторая строка]...и еще 3 тыщи строк ],
                   columns=['catalog', 'category', 'art', 'eurocode', 'oldcode', 'name', 'client_price'])
'''

# df1 = pd.DataFrame([['a', 'b'], ['c', 'd']],
#                    index=['row 1', 'row 2'],
#                    columns=['col 1', 'col 2'])
# df1.to_excel("output.xlsx")


# for json_data in json_local:
#     pprint.pprint(json_data)

