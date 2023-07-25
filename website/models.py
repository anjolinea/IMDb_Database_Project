from . import DB
from flask_login import UserMixin

class UserAuth(UserMixin):
    def __init__(self, username, userPasswordHash):
        self.id = username
        self.password = userPasswordHash
    def get(self):
        return (self.id, self.password)