from flask import Blueprint, render_template, request
from . import DB
from flask_login import login_required, current_user

views = Blueprint('views', __name__)

N = 4
ROW_LIMIT = 4


def split_moviechunks(movies, n, row_limit):
    return [movies[i * n:(i + 1) * n] for i in range((len(movies) + n - 1) // n)][:row_limit]


@views.route('/')
@login_required
def home():
    db = DB()

    query = """
    SELECT * FROM Movie ORDER BY movieRating DESC
    """
    movies = db.execute(query).fetchall()
    moviechunks = split_moviechunks(movies, N, ROW_LIMIT)

    db.close()
    return render_template('home.html', moviechunks=moviechunks, user=current_user)


@views.route('/search', methods=["GET", "POST"])
@login_required
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
        return render_template('search.html', moviechunks=moviechunks, moreLeft=moreLeft, genre_names=genre_names, title=title, actor=actor_name, genre=genre_name, sort_by=sort_by,  user=current_user)
    else:
        genre_name = request.form.get("genre")
        query = f"""
        SELECT DISTINCT Movie.movieTitle, Movie.movieRating, Movie.yearReleased, Movie.runtime, Movie.posterImgLink
        FROM Movie;
        """
        movies = db.execute(query).fetchall()
        moviechunks = split_moviechunks(movies, N, ROW_LIMIT)
        moreLeft = N * ROW_LIMIT < len(movies)

        return render_template('search.html', moviechunks=moviechunks, moreLeft=moreLeft, genre_names=genre_names,
                               user=current_user)
      
@views.route('/profile', methods=["GET", "POST"])
@login_required
def profile():
    db = DB()

    is_search = False

    if request.method == "POST":
        follow = request.form.get("Follow")
        unfollow = request.form.get("Unfollow")

        first = request.form.get("first")
        last = request.form.get("last")

        if first is not None:
            firstName = first
            is_search = True

        if last is not None:
            lastName = last
            is_search = True

        if follow is not None:
    
            select_query = f"""
            SELECT * FROM Follows WHERE userID1 = '{current_user.id}' AND userID2 = '{follow}'
            """
            val = db.execute(select_query).fetchall()

            if len(val) == 0:
                print(f"followed {follow}")
                follow_query = f"""
                INSERT INTO Follows (userID1, userID2)
                VALUES ('{current_user.id}', '{follow}');
                """
                db.execute(follow_query).fetchall()
                db.commit()

        if unfollow is not None:
            print(f"unfollowed {unfollow}")
            unfollow_query = f"""
            DELETE FROM Follows
            WHERE userID1 = '{current_user.id}'
                AND userID2 = '{unfollow}';
            """
            db.execute(unfollow_query).fetchall()
            db.commit()

    following_query = f"""
    SELECT userID2 AS username, firstName, lastName, profilePicLink
    FROM Follows, User
    WHERE userID1 = '{current_user.id}' AND username = userID2
    """
    following = db.execute(following_query).fetchall()

    followers_query = f"""
    SELECT F1.userID1 AS username, firstName, lastName, profilePicLink, (
        SELECT COUNT(*) FROM Follows F2 WHERE F2.userID2 = F1.userID1 AND F2.userID1 = F1.userID2
    ) AS isFollowing
    FROM Follows F1, User
    WHERE F1.userID2 = '{current_user.id}' AND username = F1.userID1
    """
    followers = db.execute(followers_query).fetchall()

    suggested_query = f"""
    SELECT * FROM (
        WITH RECURSIVE FollowersRecursive AS (
            SELECT Follows.userID1 AS follower,
                Follows.userID2 AS follower_of_follower, 
                0 AS level
            FROM Follows
            WHERE Follows.userID1 = '{current_user.id}'
            UNION ALL
            SELECT FollowersRecursive.follower,
                Follows.userID2, 
                FollowersRecursive.level + 1
            FROM Follows
            JOIN FollowersRecursive ON 
                Follows.userID1 = FollowersRecursive.follower_of_follower
            WHERE FollowersRecursive.level < 3 AND Follows.userID2 != '{current_user.id}'
        )
        SELECT follower_of_follower AS follower, MIN(level) AS level, firstName, lastName, profilePicLink
        FROM FollowersRecursive, User
        WHERE username = follower_of_follower
        GROUP BY follower_of_follower
        ORDER BY level)
    WHERE level > 0;
    """
    suggested = db.execute(suggested_query).fetchall()

    user_info_query = f"""
    SELECT * FROM User WHERE username = '{current_user.id}'
    """
    user_info = db.execute(user_info_query).fetchall()[0]

    if is_search:
        search_query = f"""
        SELECT username, firstName, lastName, profilePicLink, (
           SELECT COUNT(*) FROM Follows WHERE userID1 = '{current_user.id}' AND userID2 = username
        ) AS isFollowing
        FROM User 
        WHERE firstName LIKE '%{firstName}%' AND lastName LIKE '%{lastName}%' AND username != '{current_user.id}'
        """
        search_results = db.execute(search_query).fetchall()
    else:
        firstName = ""
        lastName = ""
        search_results = None

    db.close()

    return render_template('profile.html', user=current_user, user_info=user_info, following=following, followers=followers, suggested=suggested, is_search=is_search, search_results=search_results, firstName=firstName, lastName=lastName)


@views.route('/recommend', methods=["GET", "POST"])
def recommend():
    db = DB()
    print(current_user.id)
    rewatch_query = f"""
    SELECT Movie.movieTitle, Movie.movieRating, Movie.yearReleased, Movie.runtime, Movie.posterImgLink
    FROM Movie
    JOIN Watched ON Movie.movieID = Watched.movieID
    WHERE Watched.userID = '{current_user.id}'
      AND Watched.likes = 1
      AND Watched.lastWatched <= DATETIME(CURRENT_DATE, '-30 day')
    ORDER BY Watched.lastWatched ASC
    LIMIT 5
    """
    again_movies = db.execute(rewatch_query).fetchall()
    for item in again_movies:
        print(item)

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
        WHERE Watched.userID = '{current_user.id}'
    )
    AND (Genre.genreID IN (
            SELECT MovieGenre.genreID
            FROM MovieGenre
            WHERE MovieGenre.movieID IN (
                SELECT Watched.movieID
                FROM Watched
                WHERE Watched.userID = '{current_user.id}' AND Watched.likes = 1
            )
        )
        OR Actor.actorID IN (
            SELECT Starred.actorID
            FROM Starred
            WHERE Starred.movieID IN (
                SELECT Watched.movieID
                FROM Watched
                WHERE Watched.userID = '{current_user.id}' AND Watched.likes = 1
            )
        )
    )
    ORDER BY Movie.movieID DESC
    LIMIT 5;
    """
    rec_unwatched_faves = db.execute(unwatch_query).fetchall()

    get_friend_query = f"""
    SELECT User.username, User.firstName, User.lastName, User.profilePicLink
    FROM (SELECT f1.userID1 user, f1.userID2 friend 
        FROM Follows f1, Follows f2
        WHERE f1.userID1 = '{current_user.id}' AND f2.userID1 = f1.userID2 AND f2.userID2 = '{current_user.id}') t1
    JOIN User ON t1.friend = User.username
    """
    following = db.execute(get_friend_query).fetchall()

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
            WHERE Watched.userID = '{current_user.id}'
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
                WHERE FavGenre.userID = '{current_user.id}'
            )
            OR Genre.genreID IN (
                SELECT FavGenre.genreID
                FROM FavGenre
                WHERE FavGenre.userID = '{second_username}'
            )
            OR Actor.actorID IN (
                SELECT FavActor.actorID
                FROM FavActor
                WHERE FavActor.userID = '{current_user.id}'
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
                               following=following, rec_two=rec_two, second_user=second_user, user=current_user, firstClicked=True)
    else:
        db.close()
        return render_template('recommend.html', again_movies=again_movies, rec_unwatched_faves=rec_unwatched_faves,
                               following=following, user=current_user, firstClicked=False)
