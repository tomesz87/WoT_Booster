import os, requests, json

from dotenv import load_dotenv
from datetime import datetime

def post_message(message: str) -> None:
    """
    Posts a message into a Discord channel via webhook. URL of Discord room is loaded from .env
    :param message: string to be posted to the discord channel
    :return:
    """
    load_dotenv()
    url=os.getenv('DISCORD_WEBHOOK')

    data = {}
    data["content"] = message
    requests.post(url=url, data=json.dumps(data), headers={"Content-Type": "application/json"})


def post_log(message: str) -> None:
    """
    Posts a message into a Discord channel via webhook. URL of Discord room is loaded from .env
    :param message: string to be posted to the discord channel
    :return:
    """
    load_dotenv()

    url=os.getenv('LOG_WEBHOOK')

    data = {}

    time_text = datetime.strftime(datetime.now(), '%Y.%m.%d %H:%M:%S')
    message = message + ': ' + time_text
    data["content"] = message

    requests.post(url=url, data=json.dumps(data), headers={"Content-Type": "application/json"})


if __name__ == '__main__':
    post_message("X")
    post_log("új log")