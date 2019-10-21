import sqlite3


def get_sqlite_cursor(file: str):
    conn = sqlite3.connect(file, check_same_thread=False)
    return conn.cursor()
