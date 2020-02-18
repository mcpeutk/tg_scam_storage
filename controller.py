class Controller:
    def __init__(self, users_management):
        self._users_management = users_management

    async def start_bot(self, chat_id):
        if (await self._users_management.get_user_by_id(chat_id) == None):
            await self._users_management.create_user(chat_id)

    async def proceed_unknown_message(self, chat_id, message):
        pass