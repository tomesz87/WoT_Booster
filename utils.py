import os

from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

def get_time() -> str:
    """
    Returns current datetime in '%Y.%m.%d %H:%M:%S' format with leading and trailing '**' to make it bold when posted to Discord
    """
    time_text = datetime.strftime(datetime.now(), '%Y.%m.%d %H:%M:%S')
    return time_text


def update_env(token_info: dict) -> str:
    """
    Updates the .env file with the token infos after extension.
    :
    param token_info: dict Info about the new token code and expiry date in timestamp
    return None
    :
    """

    application_id = os.getenv("WG_APP_ID")
    discord_webhook=os.getenv('DISCORD_WEBHOOK')
    log_webhook=os.getenv('LOG_WEBHOOK')

    wg_token = token_info['new_token']
    wg_expiry = token_info['new_expiry']

    try:
        with open(".env", "w") as f:
            f.write(f'WG_APP_ID="{application_id}"')
            f.write(f'WG_TOKEN="{wg_token}"')
            f.write(f'WG_EXPIRY={wg_expiry}')
            f.write(f'DISCORD_WEBHOOK={discord_webhook}')
            f.write(f'LOG_WEBHOOK={log_webhook}')
    except Exception as e:
        message = e
        return message

    else:
        message = ".env file updated"
        return message