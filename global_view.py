import quart.flask_patch
# import flask_login
from quart import Quart, request, redirect

import private_settings

class GlobalView:
    app = Quart(__name__)

    def __init__(self, telegram_view, manage_view):
        # self.app.secret_key = private_settings.SECRET_KEY
        # self.login_manager = flask_login.LoginManager()
        # self.login_manager.init_app(self.app)

        self._telegram_view = telegram_view
        self._manage_view = manage_view

    def run_app(self):
        @self.app.route("/", methods = ["POST", "GET"])
        async def main_route():
            if (request.method == "POST"):
                return await self._telegram_view.proceed_request(request)

        @self.app.route("/manage", methods = ["GET"])
        async def manage_panel_route():
            return await self._manage_view.proceed_request(request)

        @self.app.route("/manage", methods = ["POST"])
        async def manage_panel_route_form():
            await self._manage_view.proceed_form(await request.form)
            return redirect(request.url)

        self.app.run()