import routes.telegram_view as telegram_view
import routes.manage_view as manage_view
import routes.global_view as global_view
import controller
import models.users_management as users_management
import models.channels_management as channels_management
import models.manual_management as manual_management
import models.web_management as web_management
import services.telegram_connector as telegram_connector

if __name__ == "__main__":
    users_management = users_management.UsersManagement()
    channels_management = channels_management.ChannelsManagement()
    manual_management = manual_management.ManualManagement()
    web_management = web_management.WebManagement()

    telegram_connector = telegram_connector.TelegramConnector()

    controller = controller.Controller(users_management, channels_management, manual_management, telegram_connector)

    telegram_view = telegram_view.TelegramView(controller)
    manage_view = manage_view.ManageView(users_management, channels_management, manual_management)

    controller.set_telegram_view(telegram_view)

    global_view = global_view.GlobalView(telegram_view, manage_view, web_management)

    global_view.run_app()