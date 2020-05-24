# -*- coding: utf-8 -*-
import sqlite3

def create_db():
    con = sqlite3.connect('./database.db')
    cur = con.cursor()
    cur.execute('CREATE TABLE IF NOT EXISTS artist( name TEXT, info TEXT, concerts TEXT )')

    forbot = ["Nirvana", #forbot is example, please delete this when the data is ready
              "американський рок-гурт, Куртом Кобейном, штат Вашингтон, в 1987 році",
              "12.05.1990 - San Juan Islands, 27.05.1990 - Seattle Downtown"]

    all_artists = [] #сюди потрібно додати всю інформацію для artist database виду: [name, info, concerts]
    all_artists.append(forbot)

    for i in all_artists:
        cur.execute('INSERT INTO artist VALUES(?, ?, ?)', i)

    cur.close()
    con.commit()


def read_db(db, table, column=None):
    con = sqlite3.connect('./database.db')
    cur = con.cursor()

    query_columns = 'pragma table_info('+table+')'
    cur.execute(query_columns)
    colums_dscr = cur.fetchall()

    if column is None:
        query = 'SELECT * FROM '+table
        cur.execute(query)
        data = cur.fetchall()
    print(data)


if __name__=='__main__':
    db = './database.db'
    table = 'artist'
    column = 'name'
    create_db()
    read_db(db, table)