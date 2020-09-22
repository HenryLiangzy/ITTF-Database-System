import sqlite3

if __name__ == "__main__":
    connect = sqlite3.connect('System.db')
    cursor = connect.cursor()
    a = 'test'
    b = a
    c = a
    d = a
    cursor.execute('INSERT INTO player (playerId, playerName, playerAssoc, playerGender) VALUES (?, ?, ?, ?);', (a, b, c, d))
    cursor.close()
    connect.commit()
    connect.close()