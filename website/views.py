from flask import Blueprint, render_template, request
from . import DB

views = Blueprint('views', __name__)

N = 4
ROW_LIMIT = 4

def split_moviechunks(movies, n, row_limit):
    return [movies[i * n:(i + 1) * n] for i in range((len(movies) + n - 1) // n )][:row_limit] 

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
    if request.method == "POST":
        title = request.form.get("title")
        actor_name = request.form.get("actor")
        genre_name = request.form.get("genre")
        minimum_rating = 5 # hardcoded

        # empty string if nothing is returned

        db = DB()
        query = f"""
        SELECT DISTINCT Movie.movieTitle, Movie.movieRating, Movie.yearReleased, Movie.runtime, Movie.posterImgLink
        FROM Movie
        JOIN Starred ON Movie.movieID = Starred.movieID
        JOIN Actor ON Starred.actorID = Actor.actorID
        JOIN MovieGenre ON Movie.movieID = MovieGenre.movieID
        JOIN Genre ON MovieGenre.genreID = Genre.genreID
        WHERE Actor.actorName LIKE '%{actor_name}%'
            AND Genre.genreName LIKE '%{genre_name}%'
            AND Movie.movieTitle LIKE '%{title}%'
            AND Movie.movieRating >= {minimum_rating};
        """
        movies = db.execute(query).fetchall()
        moviechunks = split_moviechunks(movies, N, ROW_LIMIT)
        moreLeft = N * ROW_LIMIT < len(movies)

        db.close()
        return render_template('search.html', isSearch=True, moviechunks=moviechunks, moreLeft=moreLeft)
    else:
        return render_template('search.html', isSearch=False)

@views.route('/recommend', methods=["GET", "POST"])
def recommend():
    # until username session stuff works
    temp_username = "frankvanvleet88"

    db = DB()
    rewatch_query = f"""
    SELECT Movie.movieTitle, Movie.movieRating, Movie.yearReleased, Movie.runtime, Movie.posterImgLink
    FROM Movie
    JOIN Watched ON Movie.movieID = Watched.movieID
    WHERE Watched.userID = '{temp_username}'
      AND Watched.likes = 1
      AND Watched.lastWatched <= DATETIME(CURRENT_DATE, '-30 day')
    ORDER BY Watched.lastWatched ASC
    LIMIT 5
    """
    again_movies = db.execute(rewatch_query).fetchall()

    unwatch_query = f"""
    SELECT DISTINCT Movie.movieTitle, Movie.movieRating, Movie.yearReleased, Movie.runtime, Movie.posterImgLink
    FROM Movie
    JOIN MovieGenre ON Movie.movieID = MovieGenre.movieID
    JOIN Genre ON MovieGenre.genreID = Genre.genreID
    JOIN Starred ON Movie.movieID = Starred.movieID
    JOIN Actor ON Starred.actorID = Actor.actorID
    WHERE Movie.movieID NOT IN (
        SELECT Watched.movieID
        FROM Watched
        WHERE Watched.userID = '{temp_username}'
    )
    AND (Genre.genreID IN (
            SELECT MovieGenre.genreID
            FROM MovieGenre
            WHERE MovieGenre.movieID IN (
                SELECT Watched.movieID
                FROM Watched
                WHERE Watched.userID = '{temp_username}' AND Watched.likes = 1
            )
        )
        OR Actor.actorID IN (
            SELECT Starred.actorID
            FROM Starred
            WHERE Starred.movieID IN (
                SELECT Watched.movieID
                FROM Watched
                WHERE Watched.userID = '{temp_username}' AND Watched.likes = 1
            )
        )
    )
    ORDER BY Movie.movieID DESC
    LIMIT 5;
    """
    rec_unwatched_faves = db.execute(unwatch_query).fetchall()

    get_following_query = f"""
    SELECT User.username, User.firstName, User.lastName
    FROM Follows
    JOIN User ON User.username == Follows.userID2
    WHERE Follows.userID1 = '{temp_username}'
    """
    following = db.execute(get_following_query).fetchall()

    if request.method == "POST":
        second_username = request.form.get("recTwo")
        query_rec_two = f"""
        SELECT DISTINCT Movie.movieTitle, Movie.movieRating, Movie.yearReleased, Movie.runtime, Movie.posterImgLink
        FROM Movie
        JOIN MovieGenre ON Movie.movieID = MovieGenre.movieID
        JOIN Genre ON MovieGenre.genreID = Genre.genreID
        JOIN Starred ON Movie.movieID = Starred.movieID
        JOIN Actor ON Starred.actorID = Actor.actorID
        WHERE Movie.movieID NOT IN (
            SELECT Watched.movieID
            FROM Watched
            WHERE Watched.userID = '{temp_username}'
        )
        AND Movie.movieID NOT IN (
            SELECT Watched.movieID
            FROM Watched
            WHERE Watched.userID = '{second_username}'
        )
        AND (
            Genre.genreID IN (
                SELECT FavGenre.genreID
                FROM FavGenre
                WHERE FavGenre.userID = '{temp_username}'
            )
            OR Genre.genreID IN (
                SELECT FavGenre.genreID
                FROM FavGenre
                WHERE FavGenre.userID = '{second_username}'
            )
            OR Actor.actorID IN (
                SELECT FavActor.actorID
                FROM FavActor
                WHERE FavActor.userID = '{temp_username}'
            )
            OR Actor.actorID IN (
                SELECT FavActor.actorID
                FROM FavActor
                WHERE FavActor.userID = '{second_username}'
            )
        )
        ORDER BY RANDOM()
        LIMIT 5;
        """

        user_info_query = f"""
        SELECT * FROM User WHERE username = '{second_username}'
        """
        rec_two = db.execute(query_rec_two).fetchall()
        second_user = db.execute(user_info_query).fetchone()
        db.close()
        return render_template('recommend.html', again_movies=again_movies, rec_unwatched_faves=rec_unwatched_faves,
                               following=following, rec_two=rec_two, second_user=second_user, firstClicked=True)
    else:
        db.close()
        return render_template('recommend.html', again_movies=again_movies, rec_unwatched_faves=rec_unwatched_faves,
                               following=following, firstClicked=False)
