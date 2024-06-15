import functools
import time
from typing import Any, Callable, Optional


def retry(max_attempts: Optional[int] = None) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    """
    Декоратор для автоматического повторения функции в случае ошибки соединения.

    :param max_attempts: Максимальное количество попыток (для тестирования).
    """

    def decorator_retry(func: Callable[..., Any]) -> Callable[..., Any]:
        @functools.wraps(func)
        def wrapper_retry(*args: Any, **kwargs: Any) -> Any:
            attempts = 0
            while max_attempts is None or attempts < max_attempts:
                try:
                    return func(*args, **kwargs)
                except ConnectionError:
                    attempts += 1
                    print(f"Connection error occurred. Retrying {attempts} time(s)...")
                    time.sleep(1)
            raise ConnectionError(f"Failed to connect after {attempts} attempts")

        return wrapper_retry

    return decorator_retry


def unstable_function() -> None:
    raise ConnectionError("Failed to connect to the API")
