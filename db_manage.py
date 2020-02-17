import sqlite3

class UsersManagement:
    def __init__(self):
        conn = sqlite3.connect("bot.db")
        c = conn.cursor()
        c.execute("CREATE TABLE IF NOT EXISTS users (chat_id text, \
                                                     start_date text, \
                                                     last_usage_date text, \
                                                     last_action text)")
        conn.commit()
        conn.close()

