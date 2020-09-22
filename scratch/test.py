import database


if __name__ == '__main__':
    conn, cursor = database.open_database()

    tournament_id = 3421

    cursor.execute("select * from tournaments where tournamentID = ?", (tournament_id, ))
    result = cursor.fetchall()

    print('There are', len(result), 'result')
    print(result)
