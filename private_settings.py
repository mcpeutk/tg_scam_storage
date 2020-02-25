file = open("private_settings.txt", "r")
TELEGRAM_TOKEN = "bot" + file.readline()[:-1] + "/"

DB_NAME = "bot.db"

SECRET_KEY = file.readline()[:-1]

file.close()