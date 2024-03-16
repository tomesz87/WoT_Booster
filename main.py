import os

from dotenv import load_dotenv
from datetime import datetime, timedelta

from api_handler import extend_token, activate_reserves
from utils import update_env
from discord_messager import post_log

load_dotenv()

application_id = os.getenv("WG_APP_ID")
access_token = os.getenv("WG_TOKEN")
expires_at = os.getenv("WG_EXPIRY")
discord=os.getenv('DISCORD_WEBHOOK')
url=os.getenv('LOG_WEBHOOK')

BOOSTERS_TO_LAUNCH = [('BATTLE_PAYMENTS', 10), ('MILITARY_MANEUVERS', 10)]
#BOOSTERS_TO_LAUNCH = [('TACTICAL_TRAINING', 10)]

activate_reserves(BOOSTERS_TO_LAUNCH)

# If token is about to expire in 1 week, extend it and update the .env file
expiry_timestamp = int(os.getenv('WG_EXPIRY'))
if datetime.fromtimestamp(expiry_timestamp) + timedelta(weeks=-1) < datetime.now():
    extended_token = extend_token() # Extend the token and retrieve the new token along with expiry date in a dict
    message = update_env(extended_token)
    post_log(message=message)
