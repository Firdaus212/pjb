import sqlite3

def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)

    return conn

def batch_insert(conn, table, col, data):
    str_col = ','.join(tuple(col))
    str_qmark = ','.join(tuple(['?' for c in col]))
    conn.executemany("insert or ignore into "+table+"("+str_col+") values ("+str_qmark+")", data)
    conn.commit()