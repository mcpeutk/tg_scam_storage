from quart import Quart, request

class GlobalView:
    app = Quart(__name__)

    def __init__(self, telegram_view, manage_view):
        self._telegram_view = telegram_view
        self._manage_view = manage_view

    def run_app(self):
        @self.app.route("/", methods = ["POST", "GET"])
        async def main_route():
            if (request.method == "POST"):
                return await self._telegram_view.proceed_request(request)
            elif (request.method == "GET"):
                return await self._manage_view.proceed_request(request)

        self.app.run()