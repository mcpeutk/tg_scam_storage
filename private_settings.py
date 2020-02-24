file = open("private_settings.txt", "r")
TELEGRAM_TOKEN = "bot" + file.readline() + "/"

DB_NAME = "bot.db"

SECRET_KEY = file.readline()

file.close()