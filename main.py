import telegram_view
import manage_view
import global_view
import controller
import users_management
import channels_management
import manual_management
import telegram_connector

if __name__ == "__main__":
    users_management = users_management.UsersManagement()
    channels_management = channels_management.ChannelsManagement()
    manual_management = manual_management.ManualManagement()

    telegram_connector = telegram_connector.TelegramConnector()

    controller = controller.Controller(users_management, channels_management, manual_management, telegram_connector)

    telegram_view = telegram_view.TelegramView(controller)
    manage_view = manage_view.ManageView()

    controller.set_telegram_view(telegram_view)

    global_view = global_view.GlobalView(telegram_view, manage_view)

    global_view.run_app()