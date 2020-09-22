import database


def read_by_name(player_name):
    connect, cursor = database.open_database()
    cursor.execute("SELECT * FROM player WHERE playerName = ?", (player_name,))
    data_list = cursor.fetchall()
    database.close_databse(connect, cursor)

    return data_list


def read_by_id(player_id):
    connect, cursor = database.open_database()
    cursor.execute("SELECT * FROM player WHERE playerId = ?", (player_id,))
    data_list = cursor.fetchall()
    database.close_databse(connect, cursor)

    return data_list


def get_male_rank():
    connect, cursor = database.open_database()
    cursor.execute("SELECT * FROM Menrank ORDER BY score DESC")
    data_list = cursor.fetchall()
    database.close_databse(connect, cursor)

    return data_list


def get_female_rank():
    connect, cursor = database.open_database()
    cursor.execute("SELECT * FROM Womenrank ORDER BY score DESC")
    data_list = cursor.fetchall()
    database.close_databse(connect, cursor)

    return data_list


def get_team_rank(model):
    connect, cursor = database.open_database()
    if model == 1:
        cursor.execute("SELECT * FROM CountryRankMan ORDER BY score DESC")
    elif model == 2:
        cursor.execute("SELECT * FROM CountryRankWomen ORDER BY score DESC")
    data_list = cursor.fetchall()
    database.close_databse(connect, cursor)

    return data_list
