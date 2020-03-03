import private_settings

class WebManagement():
    def __init__(self):
        pass

    def get_by_id(self, user_id):
        if (user_id == 0):
            user = WebUser(private_settings.ADMIN_USERNAME, private_settings.ADMIN_PASSWORD)
            return user
        return None

    async def user_exists(self, web_user):
        if (web_user.get_username() == private_settings.ADMIN_USERNAME and web_user.get_password() == private_settings.ADMIN_PASSWORD):
            return True
        return False

class WebUser():
    is_authenticated = True
    is_active = True
    is_anonymous = False
    user_id = None
    username = None
    password = None
    role = None

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.user_id = 0

    def get_id(self):
        return self.user_id

    def get_username(self):
        return self.username

    def get_password(self):
        return self.password

    def set_id(self, user_id):
        self.user_id = user_id

    def set_username(self, username):
        self.username = username

    def set_password(self, password):
        self.password = password

