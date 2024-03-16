import os, requests, json, time, sys

from datetime import datetime
from dotenv import load_dotenv
from discord_messager import post_log, post_message
from typing import List, Tuple

load_dotenv()
application_id = os.getenv("WG_APP_ID")
access_token = os.getenv("WG_TOKEN")
expires_at = os.getenv("WG_EXPIRY")


def extend_token() -> dict:
    """
    Sends a post request to WG API that extends the session.
    Yields a new access_token
    """
    
    url = "https://api.worldoftanks.eu/wot/auth/prolongate/"

    params = {"application_id": application_id,
            "access_token": access_token}

    r = requests.post(url=url, data=params)
    
    if r.status_code == 200:
        response = r.json()
        new_access_token = response['data']['access_token']
        new_expiry_time = response['data']['expires_at']
        post_log(f"Uj token: {new_access_token} --- Érvényes: {datetime.fromtimestamp(new_expiry_time).strftime('%Y.%m.%d %H:%M:%S')}")

        extended_token = {'new_token': new_access_token,
                          'new_expiry': new_expiry_time}

        return extended_token

    else:
        post_log(r.status_code, r.json())
        print(r.status_code, r.text)

def get_reserves_list() -> None:

    url = "https://api.worldoftanks.eu/wot/stronghold/clanreserves/"

    params = {"application_id": application_id,
            "access_token": access_token}

    response = requests.post(url=url, data=params)

    with open('reserves_list_uj.json', 'w') as f:
        f.writelines(json.dumps(response.json(), indent= 4))


def get_reserve_info(reserve_type: str, reserve_level: int) -> int:
    url = "https://api.worldoftanks.eu/wot/stronghold/clanreserves/"

    params = {"application_id": application_id,
            "access_token": access_token}

    response = requests.post(url=url, data=params).json()

    for item in response['data']:
        if item['type'] == reserve_type:
            for subtype in item['in_stock']:
                if subtype["level"] == reserve_level:
                    if subtype['status'] == "ready_to_activate":
                        return 0
                    elif subtype['status'] == 'active':
                        active_till = subtype['active_till']
                        wait_in_seconds = active_till - int(time.time()) +1
                        return wait_in_seconds
                    else:
                        post_log(f"Unhandled booster status: {subtype['status']} ... quitting with sys.exit()")
                        sys.exit()


def activate_reserves(booster_list: List[Tuple]) -> None:
    url = "https://api.worldoftanks.eu/wot/stronghold/activateclanreserve/"

    try:
        for booster in booster_list:
            reserve_type, reserve_level = booster

            params = {"application_id": application_id,
                    "access_token": access_token,
                    "reserve_level": reserve_level,
                    "reserve_type": reserve_type}
            
            # check booster status and if active, wait until the expiry time before trying to activate
            wait_time_in_seconds = get_reserve_info(reserve_type=reserve_type, reserve_level=reserve_level)
            if wait_time_in_seconds > 0:
                if wait_time_in_seconds > 120:
                    post_log(f"Két percnél többet kellene várni, nézd meg @tomesz87 {wait_time_in_seconds}")
                    sys.exit()

                time.sleep(wait_time_in_seconds)
            
            r = requests.post(url=url, data=params)

            if r.status_code == 200:
                response = r.json()
                try:
                    activation_time = response['data']['activated_at']
                except Exception as e:
                    post_log(f"Activation request sent for {reserve_type}, level {reserve_level}, but operation failed")
                    sys.exit()
                else:
                    post_log(f"{reserve_type}, level {reserve_level} activated at {activation_time}")
                    
            else:
                post_log(f"Error when trying to activate reserve (inner)\n{reserve_type}, {reserve_level}\n{e}")

    except Exception as e:
        post_log(f'Error when trying to activate reserve (outer)\n{reserve_type}, {reserve_level}\n{e}')

    else:
        post_message("@here Boosterek indultak")




if __name__ == '__main__':
    # print(extend_token())
    get_reserves_list()