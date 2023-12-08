# --- Imports --- #

import sqlite3 as sql


# --- Functions --- #

def copy_table(cur, tablename: str, temp_tablename: str = "tmp"):
    cur.execute("CREATE TABLE {temp_tablename} AS SELECT * FROM {tablename}")

def move_table(cur, tablename: str, temp_tablename: str = "tmp"):
    copy_table(cur, tablename, temp_tablename)
    cur.execute("DROP TABLE {tablename}")

def get_table(cur, tablename: str) -> tuple:
    return tuple(cur.execute("SELECT * FROM {tablename}").fetchall())

def redefine_table(conn, cur,
                   tablename: str,
                   temp_tablename: str = "tmp",
                   newFieldDefs):
    move_table(cur, tablename, temp_tablename)
    cur.execute("CREATE TABLE {tablename} ({newFieldDefs})")
    cur.execute("INSERT INTO {tablename} VALUES {get_table(temp_tablename)}")
    cur.execute("DROP TABLE {temp_tablename}")
    conn.commit()
