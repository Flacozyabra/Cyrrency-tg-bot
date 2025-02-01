import requests
import logging

logger = logging.getLogger(__name__)


def get_rates():
    """Получает курс USDT к RUB с биржи garantex.org"""
    url = 'https://garantex.org/api/v2/depth?market=usdtrub'

    try:
        response = requests.get(url=url, timeout=300)
        response.raise_for_status()  # Проверка HTTP-ошибок

        price = response.json().get('asks', [{}])[0].get('price')
        if price:
            logger.info(f"Курс - {price}")
            return price
        else:
            logger.warning("Не удалось получить курс: пустой ответ")
            return None

    except requests.exceptions.RequestException as e:
        logger.error(f"Ошибка при запросе курса: {e}")
        return None
