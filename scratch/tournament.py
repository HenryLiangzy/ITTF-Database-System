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
        'Connection': 'Keep-Alive',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.8',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
    }

    print('Downloading....')
    html = session.get(url, headers=url_header, timeout=50)
    print('Done')

    if html.cookies.get_dict():
        session.cookies.update(html.cookies)

    return html


def check_exist(id, cursor):

    cursor.execute("SELECT * FROM tournaments WHERE tournamentID = ?", (id,))
    result = cursor.fetchall()

    return len(result)


def analysis_html(html_data):
    soup = BeautifulSoup(html_data, 'html.parser')
    tournament, next_link = analysis.get_tournament_list(soup)

    if len(tournament) <= 1:
        print("table empty, data not found")
        return None

    try:
        connect, cursor = database.open_database()
        for element in tournament:
            if check_exist(element[0], cursor) == 0:
                cursor.execute(
                    "INSERT INTO tournaments (tournamentID, year, tournamentName, type, kind, organizer, matches, fromTime, toTime) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                               (element[0], element[1], element[2], element[3], element[4], element[5], element[6], element[7], element[8])
                )

        database.close_databse(connect, cursor)
    except OSError as e:
        print(e)

    return next_link


if __name__ == '__main__':
    end = 0
    url = "http://results.ittf.link/index.php?option=com_fabrik&view=list&listid=1&Itemid=111&resetfilters=0&clearordering=0&clearfilters=0&limitstart1=0"
    html_session = requests.session()

    user_cookies = {
        '_ga': 'GA1.2.1528635524.1539436901',
        'templateColor': 'green',
        '_gid': 'GA1.2.1896731523.1539694916',
        '85fda785538371be518fb5b360853ad6': 'f90cfaa402114b0f977485d371678e26',
        '_gat': '1',
    }

    html_session.cookies = cookiejar_from_dict(user_cookies)

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
