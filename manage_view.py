from quart import request, render_template

class ManageView:
    
    def __init__(self):
        pass

    async def proceed_request(self, request):
        return await render_template("manage.html")

    async def proceed_form(self, form):
        pass