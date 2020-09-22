#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# last modified 2018/10/12 13:23
# By Henry Leung

from bs4 import BeautifulSoup
import re


def delete_mark(string):
    string = string.replace('\n', '').replace('\t', '')
    return string


def get_player_ranking(soup):
    table = soup.find('table', class_='table table-striped table-condensed')
    result_list = table.tbody.find_all('tr', class_='fabrik_row', recursive=False)
    data = []

    for result in result_list:
        player_name = result.find('td', class_='fab_rnk___player_id').get_text()
        player_position = result.find('td', class_='fab_rnk___position').get_text()
        player_point = result.find('td', class_='fab_rnk___points').get_text()

        player_data = [
            delete_mark(player_name), delete_mark(player_position), delete_mark(player_point)
        ]
        data.append(player_data)

    try:
        next_link_data = table.tfoot.find('ul', class_='pagination-list').find('li', class_='pagination-next')
        next_link = next_link_data.a.get('href')

        if next_link == '#':
            url = None
        else:
            url = 'http://results.ittf.link' + next_link
    except OSError as e:
        print("Exception:", e)
        url = None

    page = table.tfoot.find_all('span', class_='add-on')
    print(delete_mark(page[1].get_text()))

    return data, url


def get_tournament_list(soup):
    table = soup.form.find('table', class_='table table-striped table-bordered table-condensed table-hover')
    tbody = table.find('tbody', class_='fabrik_groupdata')
    results = tbody.find_all('tr', class_='fabrik_row', recursive=False)
    page = table.tfoot.find_all('span', class_='add-on')

    tournament_list = []

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

        profile = [
            delete_mark(tournament_id), delete_mark(year), delete_mark(tournament_name), delete_mark(tournament_type),
            delete_mark(tournament_kind), delete_mark(tournament_organizer), delete_mark(tournament_matches),
            delete_mark(tournament_from), delete_mark(tournament_to)
        ]

        tournament_list.append(profile)

    try:
        next_link_data = table.tfoot.find('ul', class_='pagination-list').find('li', class_='pagination-next ')
        next_link = next_link_data.a.get('href')

        if next_link == '#':
            url = None
        else:
            url = 'http://results.ittf.link' + next_link
    except OSError as e:
        print("Exception:", e)
        url = None

    print(delete_mark(page[1].get_text()))

    return tournament_list, url


def get_personal_data(soup):
    personal_data = soup.find('div', class_='fabrikGroup', id='group120')

    player_id = soup.find('div', id='vw_profiles___progress_ro').get_text()
    player_name = personal_data.find('div', class_='fabrikElementReadOnly', id='vw_profiles___name_ro').get_text()
    player_country = personal_data.find('div', class_='fabrikElementReadOnly', id='vw_profiles___assoc_ro').get_text()
    player_age = personal_data.find('div', class_='fabrikElementReadOnly', id='vw_profiles___age_ro').get_text()
    player_gender = personal_data.find('div', class_='fabrikElementReadOnly', id='vw_profiles___gender_ro').get_text()

    data = [
        delete_mark(player_id),
        delete_mark(player_name),
        delete_mark(player_country),
        delete_mark(player_age),
        delete_mark(player_gender)
    ]

    return data


def get_player_result(soup):
    player_result = soup.find('div', class_='fabrikGroup', id='group122')
    player_wt_result = player_result.find('div', class_='fabrikElementReadOnly', id='vw_profiles___WTresults_ro').get_text("=")
    player_other_result = player_result.find('div', class_='fabrikElementReadOnly', id='vw_profiles___Otherresults_ro').get_text("=")
    player_doubles_result = player_result.find('div', class_='fabrikElementReadOnly', id='vw_profiles___Dblsresults_ro').get_text("+")

    player_doubles_result = player_doubles_result.replace('+20', '=20').replace('+', '')

    data = [
        spilt_list(delete_mark(player_wt_result)),
        spilt_list(delete_mark(player_other_result)),
        spilt_list(delete_mark(player_doubles_result))
    ]

    return data


def spilt_list(data):
    result_list = re.split('=', data)

    return result_list


def get_player_match(soup):
    table = soup.form.find('table', class_='table table-striped table-bordered table-condensed table-hover')
    results = table.tbody.find_all('tr', class_='fabrik_row', recursive=False)
    page = table.tfoot.find_all('span', class_='add-on')

    match_list = []

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

        match_profile = [
            delete_mark(match_name), delete_mark(match_player_a), delete_mark(match_player_b),
            delete_mark(match_player_x), delete_mark(match_player_y), delete_mark(match_event),
            delete_mark(match_result_a), delete_mark(match_result_x), delete_mark(match_winner),
            delete_mark(match_winner_dbl)
        ]

        match_list.append(match_profile)

    try:
        next_link_data = table.tfoot.find('ul', class_='pagination-list').find('li', class_='pagination-next ')
        next_link = next_link_data.a.get('href')

        if next_link == '#':
            url = None
        else:
            url = 'http://results.ittf.link' + next_link
    except AttributeError as e:
        print(e)
        url = None
    except OSError as e:
        print("Exception:", e)
        url = None

    print(delete_mark(page[1].get_text()))

    return match_list, url


if __name__ == '__main__':
    html_data = open('/Users/henryliang/PycharmProjects/FYP/scratch/Players matches.htm', 'r')
    soup = BeautifulSoup(html_data, 'html.parser')
    data_list, next_link = get_player_match(soup)
    print(data_list)
