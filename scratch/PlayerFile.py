#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# last modified 2018/10/12 13:23
# By Henry Leung

import requests
import re
import time
import random
from bs4 import BeautifulSoup
import database
import analysis


def get_list():
    connect, cursor = database.open_database()
    cursor.execute("SELECT playerId FROM player")
    id_list = cursor.fetchall()
    database.close_databse(connect, cursor)

    return id_list


def get_html(id, session):
    url_header = {
        'Connection': 'Keep-Alive',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.8',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'
    }
    url = "https://results.ittf.link/index.php"
    payload = {
        'option': 'com_fabrik',
        'view': 'details',
        'formid': '99',
        'rowid': id,
        'Itemid': '226'
    }

    html = session.get(url, params=payload, headers=url_header, timeout=10)

    if html.cookies.get_dict():
        session.cookies.update(html.cookies)

    return html


def match_id(player_id):
    id = str(player_id)
    match = re.search('([0-9]+)', id)
    id_match = match.group(1)

    return id_match


def analysis_html(html_data):
    soup = BeautifulSoup(html_data, 'html.parser')
    player_profile = analysis.get_personal_data(soup)
    player_result = analysis.get_player_result(soup)

    connect, cursor = database.open_database()

    cursor.execute(
        "INSERT INTO playerProfile (playerId, playerName, playerAssco, playerGender, playerAge) VALUES (?, ?, ?, ?, ?)",
        (player_profile[0], player_profile[1], player_profile[2], player_profile[4], player_profile[3])
    )
    player_id = player_profile[0]

    for element in player_result[0]:
        cursor.execute(
            "INSERT INTO playerResult (playerId, playerResult) VALUES (?, ?)",
            (player_id, element)
        )

    for element in player_result[1]:
        cursor.execute(
            "INSERT INTO playerOtherResult (playerId, playerResult) VALUES (?, ?)",
            (player_id, element)
        )

    for element in player_result[2]:
        cursor.execute(
            "INSERT INTO playerDoubleResult (playerId, playerResult) VALUES (?, ?)",
            (player_id, element)
        )

    database.close_databse(connect, cursor)

    return


if __name__ == '__main__':
    player_id_list = get_list()
    numbers = len(player_id_list)
    html_session = requests.Session()
    times = int(input("Input the times you want to start:"))
    error_times = 0
    stop_times = 0

    while times < numbers:
        player_id = player_id_list[times][0]
        print(player_id)
        try:
            html_data = get_html(player_id, html_session)
            # analysis_html(html_data.text)
            times += 1
            percentage = times / numbers * 100
            time.sleep(random.randint(0, 2))
            print("Finish", times, "th data less ", numbers - times, " records, ID:", player_id, "profile, complete", round(percentage, 4), "%")
        except ConnectionRefusedError as e:
            stop_point_id = player_id
            stop_times = times
            print("Connection refused from the server, break point id is:", stop_point_id)
            break
        except TimeoutError as e:
            error_times += 1

            if error_times == 3:
                stop_times = times
                print("Connection time out try 5 times and fail, break, stop time is", stop_times)
                break
            else:
                stop_point_id = player_id
                print("Connection time out, break point id is:", stop_point_id, "waiting 90s and retry")
                time.sleep(90)

    print("All record download successful")