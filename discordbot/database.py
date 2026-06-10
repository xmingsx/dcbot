import sqlite3

DB_NAME = "bot.db"

def connect():
    return sqlite3.connect(DB_NAME)

def init_db():
    conn = connect()
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS users (
        user_id TEXT PRIMARY KEY,
        gems INTEGER DEFAULT 0,
        daily TEXT DEFAULT '',
        solo_count INTEGER DEFAULT 0,
        clear_count INTEGER DEFAULT 0,
        fail_count INTEGER DEFAULT 0
    )
    """)

    conn.commit()
    conn.close()
