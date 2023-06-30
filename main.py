import requests
import json
import traceback
import time
from threading import Thread, current_thread
from json import JSONDecodeError

from datetime import datetime

from tg_bot import message, send_text_message


def get_data(url):
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36"
    }

    req = requests.get(url, headers)
    res = json.loads(req.text)
    return res


def sort_workers(workers):
    global workers_notice_list
    text = False
    for worker in workers:
        if not worker['isSold']:
            if worker['nftData']['level'] == 2:
                text, workers_notice_list = worker_level_two(worker, text, workers_notice_list)
            if worker['nftData']['level'] == 3:
                text, workers_notice_list = worker_level_three(worker, text, workers_notice_list)
        if text:
            send_text_message(message, text)
            print(text, worker)
            text = False


def worker_level_two(worker, text, workers_notice_list):
    if 60 > worker['nftData']['minePower'] >= 50:
        if 11000000000000000 <= float(worker['price']) <= fifty_mp * price_coeff:
            text, workers_notice_list = create_text(worker['nftData']['minePower'], float(worker['price']),
                                                    worker['marketId'], worker['_id'], workers_notice_list)
    elif 70 > worker['nftData']['minePower'] >= 60:
        if float(worker['price']) <= sixty_mp * price_coeff:
            text, workers_notice_list = create_text(worker['nftData']['minePower'], float(worker['price']),
                                                    worker['marketId'], worker['_id'], workers_notice_list)
    elif 80 > worker['nftData']['minePower'] >= 70:
        if float(worker['price']) <= seventy_mp * price_coeff:
            text, workers_notice_list = create_text(worker['nftData']['minePower'], float(worker['price']),
                                                    worker['marketId'], worker['_id'], workers_notice_list)
    elif 90 > worker['nftData']['minePower'] >= 80:
        if float(worker['price']) <= eighty_mp * price_coeff:
            text, workers_notice_list = create_text(worker['nftData']['minePower'], float(worker['price']),
                                                    worker['marketId'], worker['_id'], workers_notice_list)
    elif 100 >= worker['nftData']['minePower'] >= 90:
        if float(worker['price']) <= ninety_mp * price_coeff:
            text, workers_notice_list = create_text(worker['nftData']['minePower'], float(worker['price']),
                                                    worker['marketId'], worker['_id'], workers_notice_list)
    return text, workers_notice_list


def worker_level_three(worker, text, workers_notice_list):
    if 110 > worker['nftData']['minePower'] >= 100:
        if float(worker['price']) <= hundred_mp * price_coeff:
            text, workers_notice_list = create_text(worker['nftData']['minePower'], float(worker['price']),
                                                    worker['marketId'], worker['_id'], workers_notice_list)
    elif 120 > worker['nftData']['minePower'] >= 110:
        if float(worker['price']) <= hundred_ten_mp * price_coeff:
            text, workers_notice_list = create_text(worker['nftData']['minePower'], float(worker['price']),
                                                    worker['marketId'], worker['_id'], workers_notice_list)
    elif 130 > worker['nftData']['minePower'] >= 120:
        if float(worker['price']) <= hundred_twenty_mp * price_coeff:
            text, workers_notice_list = create_text(worker['nftData']['minePower'], float(worker['price']),
                                                    worker['marketId'], worker['_id'], workers_notice_list)
    elif 140 > worker['nftData']['minePower'] >= 130:
        if float(worker['price']) <= hundred_thirty_mp * price_coeff:
            text, workers_notice_list = create_text(worker['nftData']['minePower'], float(worker['price']),
                                                    worker['marketId'], worker['_id'], workers_notice_list)
    elif 150 >= worker['nftData']['minePower'] >= 140:
        if float(worker['price']) <= hundred_forty_mp * price_coeff:
            text, workers_notice_list = create_text(worker['nftData']['minePower'], float(worker['price']),
                                                    worker['marketId'], worker['_id'], workers_notice_list)
    return text, workers_notice_list


def sort_spaceships(spaceships):
    global spaceships_notice_list
    text = False
    for spaceship in spaceships:
        if spaceship['nftData']['level'] == 3:
            if float(spaceship['price']) < 10000000000000000000:
                text, spaceships_notice_list = create_text(spaceship['nftData']['level'], float(spaceship['price']),
                                                       spaceship['marketId'], spaceship['_id'], spaceships_notice_list)
        if text:
            send_text_message(message, text)
            print(text)
            text = False


def create_text(mine_power, price, market_id, id, notice_list):
    if [market_id, id] not in notice_list:
        text = f"MP {mine_power}, price {price/1000000000000000000} ETL"
        notice_list.append([market_id, id])
        return text, notice_list
    else:
        return False, notice_list


def search_workers(stream_number):
    errors = []
    while True:
        try:
            workers = get_data("https://api.cryptomines.app/api/workers")
            sort_workers(workers)
        except JSONDecodeError:
            print("JSONDecodeError")
        except:
            print(traceback.print_exc())
            if traceback not in errors:
                send_text_message(message, traceback.format_exc())
                errors.append(traceback)


def search_spaceships():
    errors = []
    while True:
        try:
            spaceships = get_data(f"https://api.cryptomines.app/api/spaceships")
            sort_spaceships(spaceships)
        except JSONDecodeError:
            print("JSONDecodeError")
        except:
            print(traceback.print_exc())
            if traceback not in errors:
                send_text_message(message, traceback.format_exc())
                errors.append(traceback)


def search_fleets(ranks):
    errors = []
    while True:
        for rank in ranks:
            try:
                fleets = get_data(f"https://api.cryptomines.app/api/fleets?rank={rank}")
                sort_fleets(fleets, trading_fleets_list)
            except JSONDecodeError:
                print("JSONDecodeError")
            except:
                print(traceback.print_exc())
                if traceback not in errors:
                    send_text_message(message, traceback.format_exc())
                    errors.append(traceback)


def sort_fleets(fleets, trading_fleets_list):
    global fleets_notice_list
    text = False
    for trading_fleet in trading_fleets_list:
        for fleet in fleets:
            if fleet['nftData']['rank'] == trading_fleet[0]\
                    and fleet['nftData']['minePower'] >= trading_fleet[1]\
                    and float(fleet['price']) < trading_fleet[2] * price_coeff:
                text, fleets_notice_list = create_text(fleet['nftData']['minePower'], float(fleet['price']),
                                                        fleet['marketId'], fleet['_id'], fleets_notice_list)
            if text:
                send_text_message(message, text)
                print(text)
                text = False


def search_cheap_fleet(ranks):
    errors = []
    for rank in ranks:
        try:
            fleets = get_data(f"https://api.cryptomines.app/api/fleets?rank={rank}")
            cheapest_fleets = sort_cheapest_fleets(fleets, rank)
            cheapest_fleets_text = create_cheapest_fleets_text(cheapest_fleets)
            send_text_message(message, cheapest_fleets_text)
        except JSONDecodeError:
            print("JSONDecodeError")
        except:
            print(traceback.print_exc())
            if traceback not in errors:
                # send_text_message(message, traceback.format_exc())
                errors.append(traceback)


def sort_cheapest_fleets(fleets, rank):
    cheapest_fleets_list = []
    cheapest_fleet = 9999000000000000000000
    for interval in range(200, 3500, 100):
        for fleet in fleets:
            if interval - 100 <= fleet['nftData']['minePower'] < interval:
                if cheapest_fleet > float(fleet['price']):
                    cheapest_fleet = float(fleet['price'])
            if fleets[fleets.index(fleet)] == fleets[-1]:
                if cheapest_fleet != 9999000000000000000000:
                    cheapest_fleets_list.append([rank, interval - 100, cheapest_fleet / 1000000000000000000])
                cheapest_fleet = 9999000000000000000000
    return cheapest_fleets_list


def create_cheapest_fleets_text(cheapest_fleets_list):
    rank = "not found"
    if cheapest_fleets_list[0][0] == '2':
        rank = "C"
    elif cheapest_fleets_list[0][0] == '3':
        rank = "B"
    elif cheapest_fleets_list[0][0] == '4':
        rank = "A"
    result_text = f"Rank {rank}\n"
    for fleet in cheapest_fleets_list:
        result_text += f"{fleet[1]} MP за {fleet[2]} ETL\n"
    return result_text


def search_page():
    fleets = get_data(f"https://api.cryptomines.app/api/workers?level=2&cursor=0&limit=30000")
    print(len(fleets))
    print(fleets[-1])
    for fleet in fleets:
        if (fleet['nftData']['minePower'] > 49 and float(fleet['price']) < fifty_mp * 1000000000000000001)\
                or (fleet['nftData']['minePower'] > 59 and float(fleet['price']) < sixty_mp * 1000000000000000001)\
                or (fleet['nftData']['minePower'] > 69 and float(fleet['price']) < seventy_mp * 1000000000000000001)\
                or (fleet['nftData']['minePower'] > 79 and float(fleet['price']) < eighty_mp * 1000000000000000001)\
                or (fleet['nftData']['minePower'] > 89 and float(fleet['price']) < ninety_mp * 1000000000000000001):
            print(f"MP {fleet['nftData']['minePower']}, price {float(fleet['price'])/1000000000000000000} ETL на "
                  f"{(int((fleets.index(fleet)-1)/8))+1} странице")
            print(fleets.index(fleet))


if __name__ == "__main__":
    price_coeff = 1000000000000000001
    fifty_mp = 0
    sixty_mp = 0
    seventy_mp = 0
    eighty_mp = 0
    ninety_mp = 0.02

    hundred_mp = 0
    hundred_ten_mp = 0
    hundred_twenty_mp = 0
    hundred_thirty_mp = 0
    hundred_forty_mp = 0

    trading_fleets_list = [[2, 1400, 2.2], [3, 1600, 3,5], [4, 1600, 10], [4, 3000, 2,2], [5, 3000, 17]]

    workers_notice_list = []
    fleets_notice_list = []
    spaceships_notice_list = []

    search_page()

    # fleet_ranks = [['2', '3', '4']]
    # op_cheap_fleet_1 = Thread(target=search_cheap_fleet, args=(fleet_ranks))
    # op_cheap_fleet_1.start()

    op_fleet_1 = Thread(target=search_fleets, args=(['2', '3', '4']))
    op_fleet_1.start()

    # op_spaceship_1 = Thread(target=search_spaceships)
    # op_spaceship_1.start()

    # time.sleep(0.4)
    # op_worker_1 = Thread(target=search_workers, args=('1'))
    # op_worker_1.start()
    # time.sleep(0.4)
    # op_worker_2 = Thread(target=search_workers, args=('2'))
    # op_worker_2.start()
    # time.sleep(0.4)
    # op_worker_3 = Thread(target=search_workers, args=('3'))
    # op_worker_3.start()
    # time.sleep(0.4)
    # op_worker_4 = Thread(target=search_workers, args=('4'))
    # op_worker_4.start()
    # time.sleep(0.4)
    # op_worker_5 = Thread(target=search_workers, args=('5'))
    # op_worker_5.start()
