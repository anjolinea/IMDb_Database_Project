from flask import Flask
import sqlite3

def DB():
    conn = sqlite3.connect('website/database.db')
    conn.row_factory = sqlite3.Row
    return conn

def db_init():
    db = sqlite3.connect('website/database.db')

    with open('website/schema.sql') as f: db.executescript(f.read())
    
    cursor = db.cursor()
    cursor.execute("INSERT INTO movies (title, content) VALUES (?, ?)", ('Avengers 1', 'Desc1'))
    cursor.execute("INSERT INTO movies (title, content) VALUES (?, ?)", ('Avengers 2', 'Desc2'))
    cursor.execute("INSERT INTO movies (title, content) VALUES (?, ?)", ('Spiderman 1', 'Desc3'))
    cursor.execute("INSERT INTO movies (title, content) VALUES (?, ?)", ('Ironman 1', 'Desc4'))

    db.commit()
    db.close()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'shhhhhhh, this is a secret'

    db_init()

    from .auth import auth
    from .views import views

    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(views, url_prefix='/')

    return app