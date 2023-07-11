from flask import Flask
from flask_bootstrap import Bootstrap
import sqlite3
from load_toy_dataset import load_toy_dataset
from flask_login import LoginManager

def DB():
    conn = sqlite3.connect('toy_database.db')
    conn.row_factory = sqlite3.Row
    return conn

def db_init():
    conn = sqlite3.connect('toy_database.db')
    # uncomment this line back in if you want a fresh new toy database
    # load_toy_dataset(conn)

    conn.commit()
    conn.close()


def create_app():
    app = Flask(__name__)
    Bootstrap(app)
    app.config['SECRET_KEY'] = 'shhhhhhh, this is a secret'

    db_init()

    from .auth import auth
    from .views import views
    from .models import UserAuth

    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(views, url_prefix='/')

    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        try:
            db = DB()
            cursor = db.cursor()
            hash_password = cursor.execute('SELECT userPassword FROM User WHERE username = ?', (id,)).fetchone()[0]
            db.close()
            return UserAuth(username=id, userPasswordHash=hash_password)
        except:
            return UserAuth(username="", userPasswordHash="")

    return app