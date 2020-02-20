import telegram_view
import manage_view
import global_view
import controller
import users_management
import channels_management

if __name__ == "__main__":
    users_management = users_management.UsersManagement()
    channels_management = channels_management.ChannelsManagement()

    controller = controller.Controller(users_management, channels_management)

    telegram_view = telegram_view.TelegramView(controller)
    manage_view = manage_view.ManageView()

    controller.set_telegram_view(telegram_view)

    global_view = global_view.GlobalView(telegram_view, manage_view)

    global_view.run_app()