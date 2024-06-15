import json
import os
from typing import Union
import logging
import datetime


def setup_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(levelname)-7s - %(name)s:%(lineno)d -> %(message)s')
    logger_file_handler = logging.FileHandler(f'logs\\{datetime.datetime.now().strftime("%Y-%m-%d")}.log', encoding='utf-8')
    logger_console_handler = logging.StreamHandler()
    logger_console_handler.setFormatter(formatter)
    logger.addHandler(logger_console_handler)
    logger_file_handler.setFormatter(formatter)
    logger.addHandler(logger_file_handler)
    return logger


logger = setup_logger("utils")


def read_data_from_json(file_path: str) -> Union[list, dict]:
    """
    ## Возвращает список словарей из JSON-строки
    Аргументы:
        `data_str (str)`: Путь к JSON-файлу
    Возвращает:
        `list`: список словарей
    """
    if not os.path.exists(file_path):
        logger.error(f"Файл {file_path} не существует")
        return []

    with open(file_path, "r", encoding="utf-8") as file:
        try:
            data = json.load(file)
            if isinstance(data, list) or isinstance(data, dict):
                logger.info(f"Файл успешно загружен: {file_path}")
                return data
            else:
                logger.error(f"Некорректный формат данных в файле: {file_path}")
                return []
        except json.JSONDecodeError:
            logger.error(f"Некорректный формат данных в файле: {file_path}")
            return []
