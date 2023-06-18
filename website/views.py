from flask import Blueprint, render_template
import sqlite3

views = Blueprint('views', __name__)

@views.route('/')
def home():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    movies = conn.execute('SELECT * FROM movies').fetchall()
    conn.close()
    return render_template('home.html', movies=movies)

@views.route('/search')
def search():
    return render_template('search.html')