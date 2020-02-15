import telegram_connector
import global_view

if __name__ == "__main__":
    telegram_view = telegram_connector.TelegramConnector()

    global_view = global_view.GlobalView(telegram_view)

    global_view.run_app()