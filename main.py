import telegram_view
import manage_view
import global_view
import controller

if __name__ == "__main__":
    controller = controller.Controller()

    telegram_view = telegram_view.TelegramView(controller)
    manage_view = manage_view.ManageView()

    global_view = global_view.GlobalView(telegram_view, manage_view)

    global_view.run_app()