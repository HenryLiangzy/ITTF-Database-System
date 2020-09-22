import sqlite3
import os

db_path = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, os.pardir))

db_name = db_path + '/FYP/system.db'


class ReadData(object):

    def __init__(self, inputValue):
        self.inputValue = inputValue

    def readPlayerProfile(self):
        connect = sqlite3.connect(db_name)
        database = connect.cursor()
        player_name = self.inputValue

        database.execute('select * from player where playerName = ?', [player_name])
        result_list = database.fetchall()
        database.close()
        connect.close()

        return result_list

    def readMatchProfile(self):
        connect = sqlite3.connect(db_name)
        database = connect.cursor()
        match_name = self.inputValue

        database.execute('select * from matchList where matchName = ?', [match_name])
        result_list = database.fetchall()
        database.close()
        connect.close()

        return result_list


if __name__ == '__main__':
    print(db_name)
    ReadData.readPlayerProfile()