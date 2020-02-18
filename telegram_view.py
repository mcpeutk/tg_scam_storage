from quart import request, jsonify
import aiohttp
import json

class TelegramView:
    request_session = None

    telegram_token = ""
    telegram_url = "https://api.telegram.org/" + telegram_token

    def __init__(self, controller):
        self._controller = controller

    async def proceed_request(self, request):
        if (request.method != "POST"):
            return

        if (self.requests_session == None):
            self.request_session = aiohttp.ClientSession()

        response = await request.get_json()

        if (not "message" in response.keys()):
            return jsonify(response)

        chat_id = response["message"]["chat"]["id"]

        if (response["message"]["text"] == "/start"):
            await self._controller.start_bot(chat_id)
            await self.send_initial_keyboard(chat_id)
        elif (response["message"]["text"] == "Добавить канал в базу"):
            await self.add_scam_channel(chat_id)
        elif (response["message"]["text"] == "В главное меню"):
            await self.send_initial_keyboard(chat_id)
        elif (response["message"]["text"] == "О боте"):
            await self.send_bot_description(chat_id)
        elif (response["message"]["text"] == "Написать создателю бота"):
            await self.send_contacts(chat_id)
        else:
            await self._controller.proceed_unknown_message(chat_id, response["message"]["text"])

        await self.send_message(chat_id, "Hello!")
        
        return jsonify(response)

    async def send_message(self, chat_id, message):
        message = {
            "chat_id": chat_id,
            "text": message
        }

        url = self.telegram_url + "sendMessage"
        await self.request_session.post(url, json = message)

    async def send_initial_keyboard(self, chat_id):
        await self._controller.set_last_action(chat_id, "initial_keyboard")

        keyboard = {
            "keyboard": [
                ["Добавить канал в базу"],
                ["О боте"],
                ["Написать создателю бота"]
            ],
            "resize_keyboard": True
        }

        message = {
            "chat_id": chat_id,
            "text": "Отправьте пост из канала (или ссылку на канал), который хотите проверить\nЛибо воспользуйтесь кнопками меню",
            "reply_markup": json.dumps(keyboard)
        }

        url = self.telegram_url + "sendMessage"
        await self.request_session.post(url, json = message)

    async def add_scam_channel(self, chat_id):
        await self._controller.set_last_action(chat_id, "add_channel")
        await self.send_message(chat_id, "Отправьте ссылку на канал, юзернейм или какой-нибудь пост из этого канала")

    async def send_bot_description(self, chat_id):
        await self._controller.set_last_action(chat_id, "bot_description")
        description = "test description"

        await self.send_message(chat_id, description)

    async def send_contacts(self, chat_id):
        await self._controller.set_last_action(chat_id, "contacts")
        contacts = "@test_username"

        await self.send_message(chat_id, contacts)