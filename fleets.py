import requests
import json
import traceback
import time
from threading import Thread, current_thread
from json import JSONDecodeError

from datetime import datetime
from bs4 import BeautifulSoup

from tg_bot import message, send_text_message


def get_data(url):
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36"
    }

    req = requests.get(url, headers)
    res = json.loads(req.text)
    return res


def create_text(rank, mine_power, price, market_id, id, notice_list):
    if [market_id, id] not in notice_list:
        text = f"Rank {rank}, MP {mine_power}, price {price/1000000000000000000} ETL"
        notice_list.append([market_id, id])
        return text, notice_list
    else:
        return False, notice_list


def search_fleets():
    global fleets_notice_list
    text = False
    errors = []
    while True:
        for trading_fleet in trading_fleets_list:
            try:
                fleets = get_data(f"https://api.cryptomines.app/api/fleets?rank={trading_fleet[0]}&page=1&limit=8&sort=eternal&mpfrom={trading_fleet[1]}&mpto=12750")['data']
                for fleet in fleets:
                    if fleet['nftData']['minePower'] >= trading_fleet[1] \
                            and float(fleet['price']) <= trading_fleet[2] * price_coeff:
                        text, fleets_notice_list = create_text(trading_fleet[0], fleet['nftData']['minePower'],
                                                               float(fleet['price']), fleet['marketId'],
                                                               fleet['_id'], fleets_notice_list)
                    if text:
                        send_text_message(message, text)
                        print(text)
                        text = False
            except JSONDecodeError:
                print("JSONDecodeError")
            except:
                print(traceback.print_exc())
                if traceback not in errors:
                    send_text_message(message, traceback.format_exc())
                    errors.append(traceback)


if __name__ == "__main__":
    price_coeff = 1000000000000000001
    fleets_notice_list = []

    trading_fleets_list = [[2, 1400, 2.1], [3, 1600, 2.6], [4, 1600, 6.5], [4, 3000, 13.2], [5, 3000, 21]]

    # op_fleet_1 = Thread(target=search_fleets)
    # op_fleet_1.start()
