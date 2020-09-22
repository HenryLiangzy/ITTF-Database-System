#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# last modified 2018/10/12 13:23
# By Henry Leung

import requests
import time
import random
from bs4 import BeautifulSoup
import database
import analysis


def get_html(url, session):
    url_header = {
        'Connection': 'Keep-Alive',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.8',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'
    }

    print('Downloading....')
    html = session.get(url, headers=url_header, timeout=50)
    print('Done')

    if html.cookies.get_dict():
        session.cookies.update(html.cookies)

    return html


def analysis_html(html_data):
    soup = BeautifulSoup(html_data, 'html.parser')
    player_ranking, next_link = analysis.get_player_ranking(soup)

    if len(player_ranking) <= 1:
        print("table empty, data not found")
        return None

    try:
        connect, cursor = database.open_database()
        for element in player_ranking:
            cursor.execute("INSERT INTO playerRanking (playerName, playerPosition, playerPoints) VALUES (?, ?, ?)",
                           (element[0], element[1], element[2]))

        database.close_databse(connect, cursor)
    except OSError as e:
        print(e)

    return next_link


if __name__ == '__main__':
    end = 0
    url = 'http://results.ittf.link/index.php?option=com_fabrik&view=list&listid=70&Itemid=207&limit70=100&resetfilters=0&clearordering=0&clearfilters=0&limitstart70=600'
    html_session = requests.session()

    while end == 0:
        try:
            html_data = get_html(url, html_session)
            next_url = analysis_html(html_data.text)
            if next_url is None:
                end = 1
                break
            else:
                url = next_url

            time.sleep(random.randint(0, 3))
        except OSError as e:
            end = 1
            print(e)
            break

    print("scratch finish")
