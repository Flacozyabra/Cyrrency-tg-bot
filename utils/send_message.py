import requests
import json
import os
import logging

# создаем экземпляр логгера
logger = logging.getLogger(__name__)


def load_message_data(file_path):
    """Загружает данные сообщения (ID и текст) из файла."""
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            return json.load(file)
    return {}

def save_message_data(file_path, message_id, text):
    """Сохраняет данные сообщения (ID и текст) в файл."""
    with open(file_path, 'w') as file:
        json.dump({"message_id": message_id, "text": text}, file)

def send_message(token, chat_id, topic_id, msg):
    """Отправляет новое сообщение и возвращает его ID."""
    send_message_url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "message_thread_id": topic_id,
        "text": msg
    }
    response = requests.post(send_message_url, json=payload)
    if response.status_code == 200:
        result = response.json().get("result", {})
        return result.get("message_id")
    else:
        logger.info(f"Ошибка при отправке сообщения: {response.status_code}, {response.text}")
        return None

def pin_message(token, chat_id, message_id):
    """Закрепляет сообщение."""
    pin_message_url = f"https://api.telegram.org/bot{token}/pinChatMessage"
    payload = {
        "chat_id": chat_id,
        "message_id": message_id
    }
    response = requests.post(pin_message_url, json=payload)
    if response.status_code == 200:
        logger.info("Сообщение успешно закреплено")
    else:
        logger.info(f"Ошибка при закреплении сообщения: {response.status_code}, {response.text}")

def send_and_update_message(token, chat_id, topic_id, msg, storage_file='message_data.json'):
    """
    Отправляет или обновляет сообщение в Telegram-группе (форуме) и закрепляет его.

    :param token: Токен бота Telegram
    :param chat_id: ID группы (с отрицательным знаком)
    :param topic_id: ID темы (форума) в группе
    :param msg: Текст сообщения для отправки или обновления
    :param storage_file: Файл для сохранения ID сообщения и текста
    """
    # Загружаем сохраненные данные сообщения
    message_data = load_message_data(storage_file)
    message_id = message_data.get("message_id")
    last_text = message_data.get("text")

    if message_id and msg == last_text:
        logger.info("Текст сообщения не изменился. Обновление не требуется")
        return

    if message_id:
        # Если сообщение уже отправлено, пытаемся обновить его
        edit_message_url = f"https://api.telegram.org/bot{token}/editMessageText"
        payload = {
            "chat_id": chat_id,
            "message_id": message_id,
            "text": msg,
        }
        response = requests.post(edit_message_url, json=payload)
        if response.status_code == 200:
            logger.info('Сообщение успешно обновлено')
            save_message_data(storage_file, message_id, msg)
        else:
            error_description = response.json().get("description", "")
            if "message to edit not found" in error_description:
                logger.info('Сообщение не найдено. Отправляем новое')
                message_id = send_message(token, chat_id, topic_id, msg)
                if message_id:
                    save_message_data(storage_file, message_id, msg)
                    pin_message(token, chat_id, message_id)
            else:
                logger.info(f"Ошибка при обновлении сообщения: {response.status_code}, {response.text}")
    else:
        # Если сообщения нет, отправляем новое
        message_id = send_message(token, chat_id, topic_id, msg)
        if message_id:
            save_message_data(storage_file, message_id, msg)
            pin_message(token, chat_id, message_id)
