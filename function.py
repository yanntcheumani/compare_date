import pandas as ps
import datetime


def direction(extension_file, name_file):
    """
    :param extension_file:
    :param name_file: file name with extension (.xlsx, .xls...)
    """

    if extension_file.lower() == "excel":

        column_index = input("what is the name of the index column: ")
        column_date = input("what is the name of the date column: ")
        compare = input("what is the deadline to respect (exemple: 0 days 5:60:60): ")
        open_excel(name_file, column_index, column_date, compare)

    elif extension_file.lower() == "csv":

        column_index = input("what is the name of the index column: ")
        column_date = input("what is the name of the date column: ")
        compare = input("what is the deadline to respect (exemple: 0 days 5:60:60): ")
        open_csv(name_file, column_index, column_date, compare)

    else:
        print("sorry i can't open that file")


def open_excel(name_file, column_index, column_date, compare):
    """
    :param name_file: file name with extension (.xlsx, .xls...)
    :param column_index: name column index filter
    :param column_date: name columns dates
    :param compare: deadline between two date
    """
    try:
        df = ps.read_excel(name_file)

        filter = filters(df, column_index, column_date, compare)
        if len(filter) >= 1:
            write(filter)
        else:
            txt = open("compare.txt", "a")
            txt.write("there is no suspicious date")
            txt.close()
    except FileNotFoundError as e:
        print(e)


def open_csv(name_file, column_index, column_date, compare):
    """

    :param name_file: file name with extension (.xlsx, .xls...)
    :param column_index: name column index filter
    :param column_date: name columns dates
    :param compare: deadline between two date
    """
    df = ps.read_csv(name_file, delimiter=";")
    filter = filters(df, column_index, column_date, compare)
    if len(filter) >= 1:
        write(filter)
    else:
        txt = open("compare.txt", "a")
        txt.write("there is no suspicious date")
        txt.close()


def filters(b, column_index, column_date, compare):
    """

    :param b:
    :param column_index: name column index filter
    :param column_date: name columns dates
    :param compare: deadline between two date
    """
    try:
        result = []
        for id_users in b[column_index]:
            filters = b.loc[b[column_index] == id_users]
            dates_connexion = filters[column_date].tolist()
            j = 0
            for d in dates_connexion:
                j += 1
                for k in range(j, len(dates_connexion)):
                    date = datetime.datetime.strptime(str(dates_connexion[k]), "%Y-%m-%d %H:%M:%S")
                    diff = date - datetime.datetime.strptime(str(d), "%Y-%m-%d %H:%M:%S")
                    if diff != ps.to_timedelta(compare):
                        result.append([d, dates_connexion[k], id_users])

        return result

    except KeyError as e:
        print(e)


def write(w):
    txt = open("compare.txt", "a")
    j = 0
    for k in range(j, len(w)):
        txt.write("%s | %s | %s\n" % (w[k][0], w[k][1], w[k][2]))
    txt.close()
