import database


def get_list():
    connect, cursor = database.open_database()
    cursor.execute("SELECT * FROM matchList")
    id_list = cursor.fetchall()
    database.close_databse(connect, cursor)
    return id_list


def get_list3():
    connect, cursor = database.open_database()
    cursor.execute("SELECT * FROM matchList2018")
    rank1 = cursor.fetchall()
    database.close_databse(connect, cursor)
    return rank1


def head2head(playerA, playerB):
    s1 = get_list()
    s2 = get_list3()
    data_list = []
    for people in range(len(s1)):
        peopleindex = s1[people][2].index('(')
        peopleindex1 = s1[people][4].index('(')
        if s1[people][6] == "Men's Singles":
            if s1[people][2][0:peopleindex - 1] == playerA and s1[people][4][0:peopleindex1 - 1] == playerB:
                data_list.append(s1[people])
            elif s1[people][2][0:peopleindex - 1] == playerB and s1[people][4][0:peopleindex1 - 1] == playerA:
                data_list.append(s1[people])

    for people in range(len(s2)):
        peopleindex3 = s2[people][2].index('(')
        peopleindex4 = s2[people][4].index('(')
        if s2[people][6] == "Men's Singles":
            if s2[people][2][0:peopleindex3 - 1] == playerA and s2[people][4][0:peopleindex4 - 1] == playerB:
                data_list.append(s2[people])
            elif s2[people][2][0:peopleindex3 - 1] == playerB and s2[people][4][0:peopleindex4 - 1] == playerA:
                data_list.append(s2[people])

    return data_list


if __name__ == '__main__':
    data_list = head2head('MA Long', 'FAN Zhendong')
    print(data_list)