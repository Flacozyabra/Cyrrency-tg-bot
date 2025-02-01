import asyncio
from datetime import datetime
from time import sleep

import yaml
import logging.config

from marshmallow.utils import timestamp

from config import load_config
from utils import send_and_update_message, get_rates


# подгружаем конфиг из окружения
config = load_config('.env')


# Функция конфигурирования и запуска бота
async def main():
    # конфигурация логгера через yaml файл
    with open('logs/logging_config.yaml', 'rt') as f:
        logconfig = yaml.safe_load(f.read())

    logging.config.dictConfig(logconfig)

    # создаем экземпляр логгера
    logger = logging.getLogger(__name__)
    logger.info('Запускаем бота')

    # # тестовые логи
    # logger.debug('Лог DEBUG')
    # logger.info('Лог INFO')
    # logger.warning('Лог WARNING')
    # logger.error('Лог ERROR')
    # logger.critical('Лог CRITICAL')
    # # вывод информации о конфигурации логера
    # print(f"Root logger level: {logging.getLogger().getEffectiveLevel()}")
    # print(f"Main logger level: {logger.getEffectiveLevel()}")

    while True:
        usdt = get_rates()

        if usdt is None:
            logger.error("Не удалось получить курс")

        else:

            tm = datetime.now().strftime("%H:%M - %d.%m.%y")
            tm = str(tm)

            msg = '💵$USDT = ₽' + usdt + ' на ' + '[' + tm + ']'
            send_and_update_message(token=config.tg_bot.token,
                                    chat_id=config.tg_bot.chat_id,
                                    topic_id=config.tg_bot.topic_id,
                                    msg=msg)
            sleep_time = 300
            logger.info(f'Полет нормальный. Спим {300} секунд.')
            sleep(sleep_time)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
