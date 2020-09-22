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
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36',
        'Cookie': '_ga=GA1.2.930520018.1528698641; 85fda785538371be518fb5b360853ad6=f8f4fbf49f6a3dda609aea710ad409d4; templateColor=green; _gid=GA1.2.1395804024.1529306884'
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
    table = soup.form.find('table', class_='table table-striped table-condensed table-hover')
    results = table.tbody.find_all('tr', class_='fabrik_row', recursive=False)
    page = table.tfoot.find_all('span', class_='add-on')

    print(delete_string(page[1].get_text()), end=': ')

    tournamentList = []

    for result in results:
        tournament_id = result.find('td', class_='fab_tournaments___tournament_id').get_text()
        year = result.find('td', class_='fab_tournaments___code').get_text()
        tournament_name = result.find('td', class_='fab_tournaments___tournament').get_text()
        tournament_type = result.find('td', class_='fab_tournaments___type').get_text()
        tournament_kind = result.find('td', class_='fab_tournaments___kind').get_text()
        tournament_organizer = result.find('td', class_='fab_tournaments___organizer').get_text()
        tournament_matches = result.find('td', class_='fab_tournaments___matches').get_text()
        tournament_from = result.find('td', class_='fab_tournaments___from').get_text()
        tournament_to = result.find('td', class_='fab_tournaments___to').get_text()

        Profile = [int(delete_string(tournament_id)), delete_string(year), delete_string(tournament_name),
                   delete_string(tournament_type), delete_string(tournament_kind),
                   delete_string(tournament_organizer), delete_string(tournament_matches),
                   delete_string(tournament_from), delete_string(tournament_to)]

        tournamentList.append(Profile)

    return tournamentList


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
        tournament_id = match_profile[0]
        year = match_profile[1]
        tournament_name = match_profile[2]
        tournament_type = match_profile[3]
        tournament_kind = match_profile[4]
        tournament_organizer = match_profile[5]
        tournament_matches = match_profile[6]
        tournament_from = match_profile[7]
        tournament_to = match_profile[8]

        #print(player_id, player_name, player_assoc, player_gender)
        database.execute(
            'INSERT INTO tournaments (tournamentID, year, tournamentName, type, kind, organizer, matches, fromTime, toTime) '
            'VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);'
            , (tournament_id, year, tournament_name, tournament_type, tournament_kind, tournament_organizer, tournament_matches,
               tournament_from, tournament_to))

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