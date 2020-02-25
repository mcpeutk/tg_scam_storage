import sqlite3
import aiosqlite

import private_settings

class ChannelsManagement:
    db_name = private_settings.DB_NAME

    def __init__(self):
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        c.execute("CREATE TABLE IF NOT EXISTS channels (channel_id text, \
                                                        channel_link text, \
                                                        proofs_link text)")
        conn.commit()
        conn.close()

    async def create_channel(self, channel_id, channel_link):
        conn = await aiosqlite.connect(self.db_name)

        query = '''INSERT INTO channels VALUES (?, ?, ?)'''
        channel_data = (channel_id, channel_link, None)

        await conn.execute(query, channel_data)
        await conn.commit()
        await conn.close()

    async def set_channel_proofs(self, channel_id, proofs_link):
        conn = await aiosqlite.connect(self.db_name)

        query = '''UPDATE channels SET proofs_link = ? WHERE channel_id = ?'''
        data = (proofs_link, channel_id)

        await conn.execute(query, data)
        await conn.commit()
        await conn.close()

    async def get_channel_by_link(self, link):
        conn = await aiosqlite.connect(self.db_name)

        query = '''SELECT * FROM channels WHERE channel_link = ?'''
        data = (link,)
        c = await conn.execute(query, data)

        result = await c.fetchall()

        await c.close()
        await conn.close()

        if (len(result) == 0):
            return None
        return result[0]

    async def get_channel_by_id(self, channel_id):
        conn = await aiosqlite.connect(self.db_name)

        query = '''SELECT * FROM channels WHERE channel_id = ?'''
        data = (channel_id,)
        c = await conn.execute(query, data)

        result = await c.fetchall()

        await c.close()
        await conn.close()

        if (len(result) == 0):
            return None
        return result[0]

    async def select_all_channels(self):
        conn = await aiosqlite.connect(self.db_name)

        query = '''SELECT * FROM channels'''

        c = await conn.execute(query)

        result = await c.fetchall()

        await c.close()
        await conn.close()

        if (len(result) == 0):
            return None
        return result

if __name__ == "__main__":
    import asyncio

    channels_management = ChannelsManagement()
    asyncio.run(channels_management.create_channel(1, "@testlink"))
    res = asyncio.run(channels_management.select_all_channels())
    # get_channel_by_id