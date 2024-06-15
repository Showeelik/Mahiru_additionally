from unittest.mock import patch, call
import pytest
from src.decorators import retry


@pytest.fixture
def decorated_unstable_function():
    return retry(max_attempts=5)

def test_retry_success_after_failures(decorated_unstable_function):
    with patch('decorators.unstable_function', side_effect=[ConnectionError, ConnectionError, 'Success!']) as mock_func:
        decorated_func = decorated_unstable_function(mock_func)
        result = decorated_func()
        assert result == 'Success!'
        assert mock_func.call_count == 3

def test_retry_exceeds_max_retries(decorated_unstable_function):
    with patch('decorators.unstable_function', side_effect=ConnectionError) as mock_func:
        decorated_func = decorated_unstable_function(mock_func)
        with pytest.raises(ConnectionError):
            decorated_func()
        assert mock_func.call_count == 5

def test_retry_waits_between_attempts(decorated_unstable_function):
    with patch('decorators.unstable_function', side_effect=ConnectionError) as mock_func, \
         patch('time.sleep', return_value=None) as sleep_mock:
        decorated_func = decorated_unstable_function(mock_func)
        with pytest.raises(ConnectionError):
            decorated_func()
        assert mock_func.call_count == 5
        assert sleep_mock.call_count == 5
        sleep_mock.assert_has_calls([call(1), call(1), call(1), call(1)])