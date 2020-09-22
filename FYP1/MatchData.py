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
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Accept-Encoding': 'gzip, deflate',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/11.1.1 Safari/605.1.15',
        'Cookie': '_ga=GA1.2.327590333.1528680236; _gid=GA1.2.2034975766.1529221699; templateColor=green; 85fda785538371be518fb5b360853ad6=dce67a7b0cd5c5b5423cf587b2f7aab6'
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


def delete_string(string):
    string = string.replace('\n', '').replace('\t', '')
    return string


def get_profile(html_data):

    soup = BeautifulSoup(html_data, 'html.parser', from_encoding='utf-8')
    table = soup.form.find('table', class_='table table-striped table-bordered table-condensed table-hover')
    results = table.tbody.find_all('tr', class_='fabrik_row', recursive=False)
    page = table.tfoot.find_all('span', class_='add-on')

    print(delete_string(page[1].get_text()), end='')

    matchList = []

    for result in results:
        match_name = result.find('td', class_='fab_matches___tournament_id').get_text()
        match_player_a = result.find('td', class_='fab_matches___name_a').get_text()
        match_player_b = result.find('td', class_='fab_matches___name_b').get_text()
        match_player_x = result.find('td', class_='fab_matches___name_x').get_text()
        match_player_y = result.find('td', class_='fab_matches___name_y').get_text()
        match_event = result.find('td', class_='fab_matches___event').get_text()
        match_result_a = result.find('td', class_='fab_matches___res_a').get_text()
        match_result_x = result.find('td', class_='fab_matches___res_x').get_text()
        match_winner = result.find('td', class_='fab_matches___winner_name').get_text()
        match_winner_dbl = result.find('td', class_='fab_matches___winners_names').get_text()

        matchProfile = [delete_string(match_name), delete_string(match_player_a), delete_string(match_player_b),
                        delete_string(match_player_x), delete_string(match_player_y), delete_string(match_event),
                        delete_string(match_result_a), delete_string(match_result_x), delete_string(match_winner),
                        delete_string(match_winner_dbl)]

        matchList.append(matchProfile)

    return matchList


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


def save_match_profile(profile_data):
    connect = sqlite3.connect('System.db')
    database = connect.cursor()
    for match_profile in profile_data:
        match_name = match_profile[0]
        match_player_a = match_profile[1]
        match_player_b = match_profile[2]
        match_player_x = match_profile[3]
        match_player_y = match_profile[4]
        match_event = match_profile[5]
        match_result_a = match_profile[6]
        match_result_x = match_profile[7]
        match_winner = match_profile[8]
        match_winner_dbl = match_profile[9]

        #print(player_id, player_name, player_assoc, player_gender)
        database.execute(
            'INSERT INTO matchList (matchName, playerA, playerB, playerX, playerY, event, resultA, resultX, winner, winnerDBL) '
            'VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?);'
            , (match_name, match_player_a, match_player_b, match_player_x, match_player_y, match_event, match_result_a,
               match_result_x, match_winner, match_winner_dbl))

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
        save_match_profile(profile_data)
        print("Done!")
        if get_next_link(url_data) is False:
            end = True
        else:
            url = get_next_link(url_data)

        time.sleep(random.randint(0, 5))

    print('Scratch data end')