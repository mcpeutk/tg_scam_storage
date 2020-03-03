import aiohttp
import json

import private_settings

class TelegramConnector:

    telegram_token = private_settings.TELEGRAM_TOKEN
    telegram_url = "https://api.telegram.org/" + telegram_token

    def __init__(self):
        pass

    async def get_channel(self, username_or_id):
        query = self.telegram_url + "getChat?chat_id=" + username_or_id

        request_session = aiohttp.ClientSession()

        response = await request_session.get(query)

        await request_session.close()

        if (response.status != 200):
            return None

        json_data = json.loads(await response.text())

        if (not json_data["ok"]):
            return None

        return json_data["result"]["id"]


if __name__ == "__main__":
    import asyncio

    telegram_connector = TelegramConnector()

    res = asyncio.run(telegram_connector.get_channel("@telegram"))
    print(res)