from flask import Blueprint, render_template, request
from . import DB

views = Blueprint('views', __name__)

N = 4
ROW_LIMIT = 4


def split_moviechunks(movies, n, row_limit):
    return [movies[i * n:(i + 1) * n] for i in range((len(movies) + n - 1) // n)][:row_limit]


@views.route('/')
def home():
    db = DB()

    query = """
    SELECT * FROM Movie ORDER BY movieRating DESC
    """
    movies = db.execute(query).fetchall()
    moviechunks = split_moviechunks(movies, N, ROW_LIMIT)

    db.close()
    return render_template('home.html', moviechunks=moviechunks)


@views.route('/search', methods=["GET", "POST"])
def search():
    db = DB()
    query_genres = """
        SELECT Genre.genreName FROM Genre
        """
    genres = db.execute(query_genres).fetchall()
    genre_names = [genre[0] for genre in genres]

    if request.method == "POST":
        title = request.form.get("title")
        actor_name = request.form.get("actor")
        genre_name = request.form.get("genre")
        sort_by = request.form.get("sort-by")
        minimum_rating = 5  # hardcoded

        # empty string if nothing is returned

        query = f"""
        SELECT DISTINCT Movie.movieTitle, Movie.movieRating, Movie.yearReleased, Movie.runtime, Movie.posterImgLink
        FROM Movie
        JOIN Starred ON Movie.movieID = Starred.movieID
        JOIN Actor ON Starred.actorID = Actor.actorID
        JOIN MovieGenre ON Movie.movieID = MovieGenre.movieID
        JOIN Genre ON MovieGenre.genreID = Genre.genreID
        WHERE Actor.actorName LIKE '%{actor_name}%'
            AND Movie.movieTitle LIKE '%{title}%'
            AND Movie.movieRating >= {minimum_rating}
        """

        if genre_name == "all":
            print(genre_name)
            query += ""
        else:
            query += f"AND Genre.genreName LIKE '%{genre_name}%'"

        if sort_by == "rating_asc":
            query += f"ORDER BY Movie.movieRating ASC"
        elif sort_by == "rating_desc":
            query += f"ORDER BY Movie.movieRating DESC"
        elif sort_by == "year_asc":
            query += f"ORDER BY Movie.yearReleased ASC"
        elif sort_by == "year_desc":
            query += f"ORDER BY Movie.yearReleased DESC"
        elif sort_by == "runtime_asc":
            query += f"ORDER BY Movie.runtime ASC"
        elif sort_by == "runtime_desc":
            query += f"ORDER BY Movie.runtime DESC"

        movies = db.execute(query).fetchall()
        moviechunks = split_moviechunks(movies, N, ROW_LIMIT)
        moreLeft = N * ROW_LIMIT < len(movies)

        db.close()
        return render_template('search.html', moviechunks=moviechunks, moreLeft=moreLeft, genre_names=genre_names)
    else:
        genre_name = request.form.get("genre")
        query = f"""
        SELECT DISTINCT Movie.movieTitle, Movie.movieRating, Movie.yearReleased, Movie.runtime, Movie.posterImgLink
        FROM Movie;
        """
        movies = db.execute(query).fetchall()
        moviechunks = split_moviechunks(movies, N, ROW_LIMIT)
        moreLeft = N * ROW_LIMIT < len(movies)

        return render_template('search.html',  moviechunks=moviechunks, moreLeft=moreLeft, genre_names=genre_names)
