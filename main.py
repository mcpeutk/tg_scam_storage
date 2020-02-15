import telegram_view
import manage_view
import global_view

if __name__ == "__main__":
    telegram_view = telegram_view.TelegramView()
    manage_view = manage_view.ManageView()

    global_view = global_view.GlobalView(telegram_view, manage_view)

    global_view.run_app()