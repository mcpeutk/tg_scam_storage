from quart import request, render_template

class ManageView:
    
    def __init__(self, users_management, channels_management, manual_management):
        self._users_management = users_management
        self._channels_management = channels_management
        self._manual_management = manual_management

    async def proceed_request(self, request):
        users = await self._users_management.select_all_users()
        channels = await self._channels_management.select_all_channels()
        manual_requests = await self._manual_management.select_all_requests()

        return await render_template("manage.html", users = users, 
                                                    channels = channels, 
                                                    manual_requests = manual_requests)

    async def proceed_form(self, form):
        if ("delete_manual_request" in form):
            await self._manual_management.remove_channel_proofs_request(form["rowid"])
            await self._manual_management.remove_channel_creation_request(form["rowid"])
        elif ("add_channel" in form):
            await self._channels_management.create_channel(form["channel_id"], form["channel_link"])
            await self._channels_management.set_channel_proofs(form["channel_link"], form["proofs_link"])