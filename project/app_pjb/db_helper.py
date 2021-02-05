import sqlite3

def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)

    return conn

def batch_insert(conn, table, data):
    conn.executemany("insert into "+table+"(h, p, q) values (?,?,?)", data)
    conn.commit()