file = open("private_settings.txt", "r")
TELEGRAM_TOKEN = "bot" + file.readline() + "/"