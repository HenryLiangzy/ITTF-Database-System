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
from requests.cookies import cookiejar_from_dict


def get_html(url, session):
    url_header = {
        'Connection': 'keep-alive',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cache-Control': 'max-age=0',
        'Host': 'results.ittf.link',
        'Upgrade-Insecure-Requests': 'Upgrade-Insecure-Requests',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
    }

    print('Downloading....')
    html = session.get(url, headers=url_header, timeout=50)
    print('Done')

    if html.cookies.get_dict():
        session.cookies.update(html.cookies)

    return html


def analysis_html(html_data):
    soup = BeautifulSoup(html_data, 'html.parser')
    player_match, next_link = analysis.get_player_match(soup)

    if len(player_match) == 0:
        print("table empty, data not found")
        return None

    try:
        connect, cursor = database.open_database()
        for element in player_match:
            cursor.execute(
                "INSERT INTO matchList2018 (matchName, playerA, playerB, playerX, playerY, event, resultA, resultX, winner, winnerDbl) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (element[0], element[1], element[2], element[3], element[4], element[5], element[6], element[7],
                 element[8], element[9])
            )
        database.close_databse(connect, cursor)
    except OSError as e:
        print(e)

    return next_link


if __name__ == '__main__':
    end = 0
    url = "http://results.ittf.link/index.php?option=com_fabrik&view=list&listid=36&Itemid=158&limit36=200&resetfilters=0&clearordering=0&clearfilters=0&limitstart36=200"
    html_session = requests.session()
    times = 0

    user_cookies = {
        '_ga': 'GA1.2.1528635524.1539436901',
        'templateColor': 'green',
        '_gid': 'GA1.2.1896731523.1539694916',
        '85fda785538371be518fb5b360853ad6': '9033c410782095caa8b18015389de28a',
    }

    # html_session.cookies = cookiejar_from_dict(user_cookies)

    while end == 0:
        try:
            html_data = get_html(url, html_session)
            next_url = analysis_html(html_data.text)
            if next_url is None:
                print(next_url)
                end = 1
                break
            else:
                url = next_url

            time.sleep(random.randint(3, 5))
        except OSError as e:
            url = next_url
            print(url)
            end = 1
            print(e)
            break

    print("scratch finish")
