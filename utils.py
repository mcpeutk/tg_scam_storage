async def fetch_username(message):
    if "t.me" in message:
        return "@" + message[message.rfind("/") + 1:]
    if message[0] != "@":
        return "@" + message