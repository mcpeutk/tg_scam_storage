from quart import Quart, request

class GlobalView:
    app = Quart(__name__)

    def __init__(self, telegram_view):
        self._telegram_view = telegram_view

    def run_app(self):
        @self.app.route("/", methods = ["POST", "GET"])
        async def main_route():
            if (request.method == "POST"):
                return await self._telegram_view.proceed_request(request)
            elif (request.method == "GET"):
                return "Hello from bot!"

        self.app.run()