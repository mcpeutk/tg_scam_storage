from quart import request, jsonify
import aiohttp

class TelegramView:
    request_session = None

    telegram_token = ""
    telegram_url = "https://api.telegram.org/" + telegram_token

    def __init__(self):
        pass

    async def proceed_request(self, request):
        if (request.method != "POST"):
            return

        if (self.requests_session == None):
            self.request_session = aiohttp.ClientSession()

        response = await request.get_json()

        if (not "message" in response.keys()):
            return jsonify(response)

        chat_id = response["message"]["chat"]["id"]

        await self.send_message(chat_id, "Hello!")
        
        return jsonify(response)

    async def send_message(self, chat_id, message):
        message = {
            "chat_id": chat_id,
            "text": message
        }

        url = self.telegram_url + "sendMessage"
        await self.request_session.post(url, json = message)
