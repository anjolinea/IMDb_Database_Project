from . import DB
from flask_login import UserMixin

class UserAuth(UserMixin):
    def __init__(self, username, userPasswordHash):
        self.id = username
        self.password = userPasswordHash