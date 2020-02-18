import sqlite3
import aiosqlite
import datetime

class UsersManagement:
    db_name = "bot.db"

    def __init__(self):
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        c.execute("CREATE TABLE IF NOT EXISTS users (chat_id text, \
                                                     start_date text, \
                                                     last_usage_date text, \
                                                     last_action text)")
        conn.commit()
        conn.close()

    async def get_user_by_id(self, chat_id):
        conn = await aiosqlite.connect(self.db_name)

        query = '''SELECT * FROM users WHERE chat_id = ?'''
        data = (chat_id,)
        c = await conn.execute(query, data)

        result = await c.fetchall()

        await c.close()
        await conn.close()

        if (len(result) == 0):
            return None
        return result[0]

    async def create_user(self, chat_id):
        curr_time = datetime.datetime.now().strftime("%d-%m-%Y %H:%M")

        conn = await aiosqlite.connect(self.db_name)

        query = '''INSERT INTO users VALUES (?, ?, ?, ?)'''
        user_data = (chat_id, curr_time, curr_time, None)

        await conn.execute(query, user_data)
        await conn.commit()
        await conn.close()

# if __name__ == "__main__":
#     import asyncio

#     users = UsersManagement()

#     asyncio.run(users.create_user(2))

#     print(asyncio.run(users.get_user_by_id(2)))