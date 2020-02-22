import utils

class Controller:
    def __init__(self, users_management, channels_management, manual_management, telegram_connector):
        self._users_management = users_management
        self._channels_management = channels_management
        self._telegram_view = None
        self._manual_management = manual_management
        self._telegram_connector = telegram_connector

    def set_telegram_view(self, telegram_view):
        self._telegram_view = telegram_view

    async def start_bot(self, chat_id):
        if (await self._users_management.get_user_by_id(chat_id) == None):
            await self._users_management.create_user(chat_id)

    async def proceed_unknown_message(self, chat_id, message):
        last_action = await self.get_last_action(chat_id)

        if (last_action in ["start_bot", "initial_keyboard", "bot_description", "contacts"]):
            if ("t.me" in message or "@" in message):
                username = await utils.fetch_username(message)
                channel_id = await self._telegram_connector.get_channel(username)

                if (channel_id == None):
                    await self._telegram_view.send_message(chat_id, "Указанного вами канала не существует. Проверьте правльность написания юзернейма или ссылки")
                    return
                
                channel = await self._channels_management.get_channel_by_id(channel_id)
                if (channel != None):
                    proof_photo = channel[2]

                    self._telegram_view.send_message(chat_id, "Увы, но этот канал оказался в нашей базе( Подтверждения ниже:")
                    if (proof_photo != None):
                        self._telegram_view.send_file(chat_id, proof_photo)
                    else:
                        self._telegram_view.send_message("Пруфов нет, но вы держитесь")
                else:
                    await self._telegram_view.send_message(chat_id, "Такого канала нет в нашей базе. Советуем проверить его самостоятельно")
        elif (last_action == "add_channel"):
            if ("t.me" in message or "@" in message):
                username = await utils.fetch_username(message)
                channel_id = await self._telegram_connector.get_channel(username)

                if (channel_id == None):
                    await self._telegram_view.send_message(chat_id, "Указанного вами канала не существует. Проверьте правльность написания юзернейма или ссылки")
                    return
                if (await self._channels_management.get_channel_by_id(channel_id) != None):
                    await self._telegram_view.send_message(chat_id, "Указанный канал уже был добавлен в нашу базу ранее")
                    await self._telegram_view.send_initial_keyboard(chat_id)
                else:
                    await self._manual_management.add_channel_creation_request(chat_id, message)
                    await self._users_management.set_last_added_channel(chat_id, message)
                    await self._telegram_view.send_proofs_request(chat_id)
            else:
                await self._telegram_view.send_message(chat_id, "Некорректная ссылка или юзернейм канала. Пожалуйста, отправьте ссылку, которая начинается с \"t.me/\" или юзернейм, который начинается с @")
        elif (last_action == "proofs"):
            await self._telegram_view.send_message(chat_id, "Пожалуйста, отправьте боту ваши подтверждения в виде скриншота")

    async def proceed_photo(self, chat_id, photo):
        last_action = await self.get_last_action(chat_id)

        if (last_action != "proofs"):
            await self._telegram_view.send_message(chat_id, "Я не знаю как ответить на ваше сообщение. Попробуйте воспользоваться кнопками меню")
            await self._telegram_view.send_initial_keyboard(chat_id)
            return

        await self._telegram_view.send_message(chat_id, "Подтверждения и канал приняты на рассмотрение! Если у нас возникнут какие-либо вопросы или подтверждений будет недостаточно - мы обязательно вам напишем!")
        await self._telegram_view.send_initial_keyboard(chat_id)

        photo_id = photo["file_id"]

        last_added_channel = await self._users_management.get_last_added_channel(chat_id)

        await self._manual_management.add_channel_proofs_request(chat_id, last_added_channel, photo_id)

    async def set_last_action(self, chat_id, action):
        await self._users_management.set_last_usage_date(chat_id)
        await self._users_management.set_last_action(chat_id, action)

    async def get_last_action(self, chat_id):
        return await self._users_management.get_last_action(chat_id)