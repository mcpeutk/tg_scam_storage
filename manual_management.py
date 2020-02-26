import sqlite3
import aiosqlite

import private_settings

class ManualManagement:
    db_name = private_settings.DB_NAME

    def __init__(self):
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        c.execute("CREATE TABLE IF NOT EXISTS manual_requests (chat_id text, \
                                                               channel_id_message text, \
                                                               channel_id text, \
                                                               proofs_link text)")
        conn.commit()
        conn.close()

    async def add_channel_creation_request(self, chat_id, channel_id_message, channel_id):
        conn = await aiosqlite.connect(self.db_name)

        query = '''INSERT INTO manual_requests VALUES (?, ?, ?, ?)'''
        request_data = (chat_id, channel_id_message, channel_id, None)

        await conn.execute(query, request_data)
        await conn.commit()
        await conn.close()

    async def add_channel_proofs_request(self, chat_id, channel_id_message, proofs):
        conn = await aiosqlite.connect(self.db_name)

        query = '''UPDATE manual_requests SET proofs_link = ? WHERE chat_id = ? AND channel_id_message = ?'''
        data = (proofs, chat_id, channel_id_message)

        await conn.execute(query, data)
        await conn.commit()
        await conn.close()

    async def remove_channel_creation_request(self, record_id):
        conn = await aiosqlite.connect(self.db_name)

        query = '''DELETE FROM manual_requests WHERE rowid = '''
        record_data = (record_id,)

        await conn.execute(query, record_data)
        await conn.commit()
        await conn.close()

    async def remove_channel_proofs_request(self, record_id):
        conn = await aiosqlite.connect(self.db_name)

        query = '''UPDATE manual_requests SET proofs_link = ? WHERE rowid = ?'''
        data = (None, record_id)

        await conn.execute(query, data)
        await conn.commit()
        await conn.close()

    async def select_all_requests(self):
        conn = await aiosqlite.connect(self.db_name)

        query = '''SELECT rowid, chat_id, channel_id_message, channel_id, proofs_link FROM manual_requests'''

        c = await conn.execute(query)

        result = await c.fetchall()

        await c.close()
        await conn.close()

        if (len(result) == 0):
            return None
        return result
