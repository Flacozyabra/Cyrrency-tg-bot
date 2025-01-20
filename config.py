from dataclasses import dataclass
from environs import Env


@dataclass
class TgBot:
    token: str            # Токен для доступа к телеграм-боту
    admin_ids: list[int]  # Список id администраторов бота
    chat_id: str          # id группы тг
    topic_id: str         #id топика группы тг


@dataclass
class Config:
    tg_bot: TgBot


def load_config(path: str | None) -> Config:

    env: Env = Env()  # Создаем экземпляр класса Env
    env.read_env(path)  # Методом read_env() читаем файл .env и загружаем из него переменные в окружение

    return Config(tg_bot=TgBot(token=env('BOT_TOKEN'),
                               admin_ids=list(map(int, env.list('ADMIN_IDS'))),
                               chat_id=env('CHAT_ID'),
                               topic_id=env('TOPIC_ID')
                               ))
