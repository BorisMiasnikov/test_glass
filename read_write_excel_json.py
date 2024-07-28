import datetime
import json
import pandas as pd

default_url = "https://github.com/BorisMiasnikov/test_glass/raw/master/%D0%9F%D1%80%D0%B0%D0%B9%D1%81-%D0%BB%D0%B8%D1%81%D1%82%20AGC%202024.03.04%20%D0%9E%D0%BF%D1%82.xlsx"
catalog_name = {"Автостекло. Аксессуары. Клей": "Иномарки", "Российский автопром": "Российский автопром"}
category_filter = ["ветровое", "заднее", "боковое", ]
default_json_name = "price_list.json"
price_modifier = {
    "ветровое": lambda price: (price + 1000) * 1.05,
    "заднее": lambda price: (price + 800) * 1.07,
    "боковое": lambda price: price * 1.1,
}

def _get_price(value):
    if str(value["ОПТ"]) == "*":
        return float(value["Цена фиксирована"])
    else:
        return value["ОПТ"]


def _get_json_element(value: dict, sheet_name: str) -> dict:
    try:
        return {
            "art": int(value["Код AGC"]),
            "oldcode": value["Старый Код AGC"],
            "name": value["Наименование"],
            "eurocode": value["Еврокод"],
            "catalog": catalog_name[sheet_name],
            "price": _get_price(value),
            "category": value["Вид стекла"],
        }
    except Exception:
        print(value)


def _get_excel_element(value: dict) -> dict:
    return {
        "catalog": value.get("catalog"),
        "category": value.get("category"),
        "art": value.get("art"),
        "eurocode": value.get("eurocode"),
        "oldcode": value.get("oldcode"),
        "name": value.get("name"),
        "client_price": _calculate_client_price(value.get("category"), value.get("price")),
    }


def _parse_excel(data: dict) -> list[dict]:
    price_list = []
    for sheet_name in data.keys():
        current_sheet = data[sheet_name]
        for i in range(len(current_sheet)):
            sheet_row = current_sheet.iloc[i]
            if not sheet_row.isnull()["Вид стекла"] and not sheet_row.isnull()["Код AGC"]:
                price_list.append(_get_json_element(value=sheet_row, sheet_name=sheet_name))
    return price_list



def _calculate_client_price(category: str, price: float) -> float:
    return price_modifier[category](price)



def _write_json(value: list[dict], json_name: str = default_json_name):
    with open(json_name, "w", encoding="utf-8") as write_file:
        json.dump(value, write_file, ensure_ascii=False, indent=4)


def _read_json(json_name: str = default_json_name) -> list[dict]:
    with open(json_name, "r", encoding="utf-8") as json_file:
        return json.load(json_file)


def _prepare_data_for_excel(data: list[dict]) -> list[dict]:
    detail_data = []
    for i in data:
        if i.get("category") in category_filter:
            detail_data.append(_get_excel_element(value=i))
    return detail_data


def _write_excel(value: list[dict]):
    df = pd.DataFrame(data=[list(val.values()) for val in value],
                      columns=list(value[0].keys()))
    df.to_excel("client_catalog.xlsx", index=False)


def _read_excel(sheet_names: list[str], excel_url: str) -> dict:
    return pd.read_excel(
        excel_url,
        engine="openpyxl",
        sheet_name=sheet_names,
        header=4,
    )

def main(url=default_url, write=1, read=1):
    if write:
        """Решение задачи 1"""
        data_exel = _read_excel(list(catalog_name.keys()), url)
        json_data = _parse_excel(data_exel)
        _write_json(json_data)
    if read:
        """Решение задачи 2"""
        json_data = _read_json()
        data_excel = _prepare_data_for_excel(json_data)
        _write_excel(data_excel)


if __name__ == "__main__":
    main()
