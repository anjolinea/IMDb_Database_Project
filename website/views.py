from flask import Blueprint, render_template, request
from . import DB

views = Blueprint('views', __name__)

@views.route('/')
def home():
    db = DB()
    movies = db.execute('SELECT * FROM movies').fetchall()
    db.close()
    return render_template('home.html', movies=movies)

@views.route('/search', methods=["GET", "POST"])
def search():
    if request.method == "POST":
        title = request.form.get("title")
        db = DB()
        movies = db.execute('SELECT * FROM movies WHERE title LIKE ?', ('%' + title + '%',)).fetchall()
        db.close()
        return render_template('search.html', isSearch=True, movies=movies)
    else:
        return render_template('search.html', isSearch=False)