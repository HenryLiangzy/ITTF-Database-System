#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# last modified 2018/10/12 13:23
# By Henry Leung

import sqlite3


def open_database():
    connect = sqlite3.connect('final.db')
    cursor = connect.cursor()

    return connect, cursor


def close_databse(connect, cursor):
    cursor.close()
    connect.commit()
    connect.close()

    return



