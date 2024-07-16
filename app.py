import json
import pandas as pd

url_file = "https://github.com/Pahteev/test_task1/raw/main/files/%D0%9F%D1%80%D0%B0%D0%B9%D1%81-%D0%BB%D0%B8%D1%81%D1%82%20AGC%202024.03.04%20%D0%9E%D0%BF%D1%82.xlsx"
url_local = r"C:\Users\Admin\Desktop\Study\Гласс рус задание\Прайс-лист AGC 2024.03.04 Опт.xlsx"

sales = pd.read_excel(
    url_local,
    engine="openpyxl",
    sheet_name=['Автостекло. Аксессуары. Клей', "Российский автопром"],
    header=4,
)


def create_json(data):  # в дату теперь передаем весь датафрейм
    list_json = []
    for list in data.keys():
        foreign_car = data[list]
        foreign_car_supp = foreign_car[
            ["Вид стекла", "Еврокод", "Код AGC", "Старый Код AGC", "Наименование", "Цена фиксирована", "ОПТ"]]
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


with open('data_file.json', 'r', encoding='utf-8') as json_file:
    json_local = json.load(json_file)

detail_data = []
detail_columns = []


def client_price(data):
    if data['category'] == "ветровое":
        price = (float(data['price']) + 1000) + (float(data['price']) + 1000) * 0.05
        return price
    elif data['category'] == "заднее":
        price = (float(data['price']) + 800) + (float(data['price']) + 800) * 0.07
        return price
    elif data['category'] == "боковое":
        price = float(data['price']) + float(data['price']) * 0.1
        return price


for i in json_local:
    if i['category'] == "ветровое" or "заднее" or "боковое":
        detail_data_unit = []
        detail_data_unit.append(i['catalog'])
        detail_data_unit.append(i['category'])
        detail_data_unit.append(i['art'])
        detail_data_unit.append(i['eurocode'])
        detail_data_unit.append(i['oldcode'])
        detail_data_unit.append(i['name'])
        detail_data_unit.append(client_price(i))
        detail_data.append(detail_data_unit)

df1 = pd.DataFrame(detail_data,
                   columns=['catalog', 'category', 'art', 'eurocode', 'oldcode', 'name', 'client_price'])
df1.to_excel("output.xlsx")
