import datetime
import os
from typing import Any, Dict, Optional, Union

import requests

from src.decorators import retry
from src.utils import setup_logger

logger = setup_logger("external_api")


@retry()
def get_api_request(
    url: str, params: Optional[Dict[str, Any]] = None, headers: Optional[Dict[str, Any]] = None
) -> requests.Response | None:
    """## Функция для отправки запроса к API
    Аргументы:
        `url (str)`: URL API
        `params (dict)`: Параметры запроса
        `headers (dict)`: Заголовки запроса

    Возвращает:
        `requests.Response`: Ответ API
    """
    try:
        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()  # This will raise HTTPError for bad responses
        logger.info(f"API request sent to {url}")
    except requests.exceptions.ConnectionError as e:
        logger.error(f"API connection error: {e}")
        raise requests.exceptions.ConnectionError("API connection error: " + str(e))
    except requests.exceptions.HTTPError as e:
        logger.error(f"API request error: {e}")
        raise requests.exceptions.HTTPError("API request error: " + str(e))
    except requests.exceptions.Timeout as e:
        logger.error(f"API request timeout: {e}")
        raise requests.exceptions.Timeout("API request timeout: " + str(e))
    except requests.exceptions.RequestException as e:
        logger.error(f"API request error: {e}")
        raise requests.exceptions.RequestException("API request error: " + str(e))
    else:
        if not response.content:
            logger.error("API request returned an empty response")
            raise ValueError("API request returned an empty response")
    return response


def get_api_key(value: str) -> str | None:
    """## Функция для получения API ключа

    Аргументы:
        `value (str)`: Значение API ключа

    Возвращает:
        `str`: API ключ
    """
    try:
        return os.getenv(value)
    except KeyError:
        logger.error("API key not found in environment variables")
        raise KeyError("API key not found in environment variables")


def get_weather_data(city: str) -> Union[Any, None]:
    """## Функция для получения данных о погоде
    Аргументы:
        `city (str)`: Город

    Возвращает:
        `dict`: Данные о погоде
    """
    api_url = "https://api.openweathermap.org/data/2.5/weather"
    params = {"q": city, "units": "metric", "lang": "ru", "appid": get_api_key("API_KEY_OPENWEATHER")}

    response = get_api_request(api_url, params=params)
    if not response:
        logger.error("API request failed")
        return None
    logger.info("API request successful")
    data = response.json()
    return data


def output_data(city: str) -> None:
    """## Функция для вывода данных о погоде
    Аргументы:
        `city (str)`: Город
    """
    data = get_weather_data(city)
    if not data:
        logger.error("Ошибка при получении данных о погоде.")
        return

    timezone = datetime.timezone(datetime.timedelta(seconds=data["timezone"]))

    print(f"Погода в городе {city}:")
    print(f"Дата: {datetime.datetime.now(timezone).strftime('%Y-%m-%d')}")
    print(f"Время: {datetime.datetime.now(timezone).strftime('%H:%M:%S')}")
    print(f"Описание: {data['weather'][0]['description']}")
    print(f"Температура: {data['main']['temp']} °C")
    print(f"Ощущается как: {data['main']['feels_like']} °C")
    print(f"Максимальная температура: {data['main']['temp_max']} °C")
    print(f"Минимальная температура: {data['main']['temp_min']} °C")
    print(f"Влажность: {data['main']['humidity']}%")
    print(f"Скорость ветра: {data['wind']['speed']} м/с")
    print(f"Видимость: {data['visibility']} м")
    print(f"Давление: {data['main']['pressure']} мм рт.ст.")
