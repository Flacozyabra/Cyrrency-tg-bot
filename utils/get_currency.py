import requests
import logging

# создаем экземпляр логгера
logger = logging.getLogger(__name__)


def get_rates():

        # URL для получения информации о курсах
    url = 'https://garantex.org/api/v2/depth?market=usdtrub'

    # Отправляем GET-запрос
    response = requests.get(url=url)

    # Проверяем, что запрос успешен
    if response.status_code == 200:
        logger.info(f"Курс - {response.json()['asks'][0]['price']}")
        return response.json()['asks'][0]['price']
    else:
        logger.info(f"Ошибка при запросе курса: {response.status_code}")
