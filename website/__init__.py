from flask import Flask
import sqlite3
from load_toy_dataset import load_toy_dataset

def DB():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

def db_init():
    conn = sqlite3.connect('database.db')
    load_toy_dataset(conn)

    conn.commit()
    conn.close()


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'shhhhhhh, this is a secret'

    db_init()

    from .auth import auth
    from .views import views

    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(views, url_prefix='/')

    return app