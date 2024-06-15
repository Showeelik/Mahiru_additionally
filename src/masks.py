import datetime
from typing import Any, Dict, Union

from src.utils import read_data_from_json, setup_logger

logger = setup_logger("masks")


def calculate_sales_by_day_of_week(data: Union[dict, list]) -> Dict[str, float]:
    """
    ## Вычисляет общую сумму продаж за каждый день недели.

    Аргументы:
        data (List[Dict[str, Any]]): Список словарей с данными о продажах.

    Возвращает:
        Dict[str, float]: Словарь, где ключи - дни недели, а значения - общая сумма продаж за этот день.
    """
    sales_by_day: dict[Any, Any] = {}
    for sale in data:
        date = datetime.datetime.strptime(sale["date"], "%Y-%m-%d")
        day_of_week = date.strftime("%A")
        price = sale["price"]
        quantity = sale["quantity"]
        total_price = price * quantity
        if day_of_week in sales_by_day:
            sales_by_day[day_of_week] += total_price
        else:
            sales_by_day[day_of_week] = total_price
    return sales_by_day


def output_price_day_week_data_json() -> None:
    """
    ### Выводит в консоль общую сумму продаж за каждый день недели.
    """

    data = read_data_from_json("data\\data.json")
    sales_by_day = calculate_sales_by_day_of_week(data)
    for day, total_price in sales_by_day.items():
        print(f"День недели: {day}, Общая сумма продаж: {total_price}")
