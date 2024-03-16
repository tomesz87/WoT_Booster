from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

def update_env() -> None:
    with open(".env", "w") as f:
        f.write


def get_time() -> str:
    time_text = datetime.strftime(datetime.now(), '%Y.%m.%d %H:%M:%S')
    return time_text