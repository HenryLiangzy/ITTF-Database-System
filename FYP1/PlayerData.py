#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# last modified 2018/06/11 10:23
# By Henry Leung

import urllib.request
import time
import random
from bs4 import BeautifulSoup
import sqlite3


def add_head(url):
    url_full = urllib.request.Request(url, headers={
        'Connection': 'Keep-Alive',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.8',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'
    })
    return url_full


def get_html(url):
    try:
        url_data = urllib.request.urlopen(url, timeout=50).read()
        url_data = url_data.decode('UTF-8')

        return url_data
    except:
        print('Open url fail')


def save_html(html_data, file_name):
    try:
        file_data = open(file_name + '.html', 'w')
        file_data.write(html_data)
        file_data.close()
        print("Save file successful")
    except:
        print("fail to save file")


def delete_mark(string):
    string = string.replace('\n', '').replace('\t', '')
    return string


def get_profile(html_data):

    soup = BeautifulSoup(html_data, 'html.parser', from_encoding='utf-8')
    results = soup.tbody.find_all('tr', class_='fabrik_row')
    table = soup.find('table', class_='table-hover')
    page = table.tfoot.find_all('span', class_='add-on')

    print(delete_mark(page[1].get_text()))

    allProfile = []

    for result in results:
        player_id = result.find('td', class_='vw_profiles___player_id').get_text()
        player_name = result.find('td', class_='vw_profiles___name').get_text()
        player_assoc = result.find('td', class_='vw_profiles___assoc').get_text()
        player_gender = result.find('td', class_='vw_profiles___gender').get_text()

        playerProfile = [delete_mark(player_id), delete_mark(player_name), delete_mark(player_assoc), delete_mark(player_gender)]
        allProfile.append(playerProfile)

    return allProfile


def get_next_link(html_data):
    soup = BeautifulSoup(html_data, 'html.parser', from_encoding='utf-8')

    next_exist = soup.find('ul', class_='pagination-list').find('li', class_='pagination-next active')

    next_link_data = soup.find('ul', class_='pagination-list').find('li', class_='pagination-next')
    next_link = next_link_data.a.get('href')

    if next_link == '#':
        return False
    else:
        next_link = 'http://results.ittf.link' + next_link
        return next_link


def save_player_profile(profile_data):
    connect = sqlite3.connect('System.db')
    database = connect.cursor()
    for player_prifile in profile_data:
        player_id = player_prifile[0]
        player_name = player_prifile[1]
        player_assoc = player_prifile[2]
        player_gender = player_prifile[3]

        #print(player_id, player_name, player_assoc, player_gender)
        database.execute(
            'INSERT INTO player (playerId, playerName, playerAssoc, playerGender) VALUES (?, ?, ?, ?);'
            , (player_id, player_name, player_assoc, player_gender))

    database.close()
    connect.commit()
    connect.close()


if __name__ == '__main__':
    url = input("Input url:")
    end = False

    while end is False:
        url = add_head(url)
        url_data = get_html(url)
        profile_data = get_profile(url_data)
        save_player_profile(profile_data)
        if get_next_link(url_data) is False:
            end = True
        else:
            url = get_next_link(url_data)

        time.sleep(random.randint(0, 2))

    print('Scratch data end')