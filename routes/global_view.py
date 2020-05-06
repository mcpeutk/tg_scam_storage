import quart.flask_patch
import flask_login
import asyncio
from quart import Quart, request, redirect, render_template

import sys
sys.path.append("..")

import models.web_management as web_management
import private_settings

class GlobalView:
    app = Quart(__name__, template_folder="../templates")

    def __init__(self, telegram_view, manage_view, web_management):
        self.app.secret_key = private_settings.SECRET_KEY
        self.login_manager = flask_login.LoginManager()
        self.login_manager.init_app(self.app)

        self._telegram_view = telegram_view
        self._manage_view = manage_view
        self._web_management = web_management

    def run_app(self):
        @self.app.route("/", methods = ["POST", "GET"])
        async def main_route():
            if (request.method == "POST"):
                return await self._telegram_view.proceed_request(request)
            else:
                return "Hello from bot!"

        @self.app.route("/manage", methods = ["GET"])
        @flask_login.login_required
        async def manage_panel_route():
            return await self._manage_view.proceed_request(request)

        @self.app.route("/manage", methods = ["POST"])
        @flask_login.login_required
        async def manage_panel_route_form():
            await self._manage_view.proceed_form(await request.form)
            return redirect(request.url)

        @self.app.route("/login", methods=["GET", "POST"])
        async def login():
            if (request.method == "GET"):
                return await render_template("login.html")
            else:
                form = await request.form
                web_user = web_management.WebUser(form["username"], form["password"])

                if (await self._web_management.user_exists(web_user)):
                    flask_login.login_user(web_user)
                    return quart.redirect("/manage")
                return await render_template("login.html")
        
        @self.login_manager.user_loader
        def load_user(user_id):
            return asyncio.get_event_loop().sync_wait(self._web_management.get_by_id(user_id))

        self.app.run()