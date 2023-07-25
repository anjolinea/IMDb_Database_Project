from flask import Blueprint, render_template, request
from . import DB
from flask_login import login_required, current_user
from rapidfuzz import process
from datetime import datetime
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

    if request.method == "POST":
        formatted_date = datetime.now().date().strftime('%Y-%m-%d')
        likes = 0
        movID = None
        fav = request.form.get("fav")
        updateDate = False

        if fav is not None:
            movID = request.form.get("movId")
            likes = fav
        print("FAV", fav)
        print("movID:", movID)
        
        addWatched = request.form.get("watched")
        print("watched", addWatched)
        if addWatched is not None:
            movID = addWatched
            updateDate = True

        print("ID:", movID)

        if movID is not None:
            print("ADDING INPUT")
            select_query = f"""
            SELECT * FROM Watched WHERE userID = '{current_user.id}' AND movieID = '{movID}'
            """
            val = db.execute(select_query).fetchall()

            if len(val) == 0:
                print("Inserting into watched")
                watched_query = f"""
                INSERT INTO Watched (userID, movieID, lastWatched, likes)
                VALUES ('{current_user.id}', '{movID}', '{formatted_date}', '{likes}');
                """
            elif updateDate:
                print("Updating watched with date")
                watched_query = f"""
                UPDATE Watched
                SET lastWatched = {formatted_date}
                WHERE userID = '{current_user.id}' AND movieID = '{movID}';
                """
            else:
                print("Updating watched with likes")
                watched_query = f"""
                UPDATE Watched
                SET likes = {likes}
                WHERE userID = '{current_user.id}' AND movieID = '{movID}';
                """
            db.execute(watched_query).fetchall()
            db.commit()

    query_genres = """
        SELECT Genre.genreName FROM Genre
        """
    genres = db.execute(query_genres).fetchall()
    genre_names = [genre[0] for genre in genres]

    # get movies
    query_movies = """
        SELECT Movie.movieTitle FROM Movie
        """
    movies = db.execute(query_movies).fetchall()
    movie_titles = [title[0] for title in movies]

    # get actor names
    query_actors = """
        SELECT Actor.actorName FROM Actor
        """
    actors = db.execute(query_actors).fetchall()
    actors = [actor[0] for actor in actors]

    # sort by fields
    sort_by_fields = ["Rating (Ascending)", "Rating (Descending)", "Year Released (Ascending)",
                      "Year Released (Descending)", "Runtime (Ascending)", "Runtime (Descending)"]

    if request.method == "POST":
        title = request.form.get("title")
        actor_name = request.form.get("actor")
        genre_name = request.form.get("genre")
        sort_by = request.form.get("sort_by")
        minimum_rating = 5  # hardcoded

        query = f"""
        SELECT DISTINCT Movie.movieTitle, Movie.movieRating, Movie.yearReleased, Movie.runtime, Movie.posterImgLink, Movie.movieID,
        Watched.likes, (SELECT COUNT(*) FROM Watched WHERE Movie.movieID = Watched.movieID AND Watched.userID = '{current_user.id}') AS watch
        FROM Movie
        JOIN Starred ON Movie.movieID = Starred.movieID
        JOIN Actor ON Starred.actorID = Actor.actorID
        JOIN MovieGenre ON Movie.movieID = MovieGenre.movieID
        JOIN Genre ON MovieGenre.genreID = Genre.genreID
        LEFT JOIN Watched ON Movie.movieID = Watched.movieID AND Watched.userID = '{current_user.id}'
        WHERE Actor.actorName LIKE '%{actor_name}%'
                AND Movie.movieTitle LIKE '%{title}%'
                AND Movie.movieRating >= {minimum_rating}
        """

        searched_query = db.execute(query).fetchall()
        query_results = [title[0] for title in searched_query]

        fuzzed_titles = []
        fuzzed_names = []
        if len(query_results) == 0:
            if title != "":
                fuzzed_titles = [title[0]
                                 for title in process.extract(title, movie_titles) if title[1] > 75]
            if actor_name != "":
                fuzzed_names = [name[0]
                                for name in process.extract(actor_name, actors)]
            # if no match
            if len(fuzzed_titles) == 0:
                fuzzed_titles = [title]
            if len(fuzzed_names) == 0:
                fuzzed_names = [actor_name]
            print(fuzzed_titles)
            print(fuzzed_names)
            query = f"""
            SELECT DISTINCT Movie.movieTitle, Movie.movieRating, Movie.yearReleased, Movie.runtime, Movie.posterImgLink, Movie.movieID,
            Watched.likes, (SELECT COUNT(*) FROM Watched WHERE Movie.movieID = Watched.movieID AND Watched.userID = '{current_user.id}') AS watch
            FROM Movie
            JOIN Starred ON Movie.movieID = Starred.movieID
            JOIN Actor ON Starred.actorID = Actor.actorID
            JOIN MovieGenre ON Movie.movieID = MovieGenre.movieID
            JOIN Genre ON MovieGenre.genreID = Genre.genreID
            LEFT JOIN Watched ON Movie.movieID = Watched.movieID AND Watched.userID = '{current_user.id}';
            """
            other_titles = ""
            other_names = ""
            for i in range(1, len(fuzzed_titles)):
                other_titles += f"""
                OR Movie.movieTitle LIKE '%{fuzzed_titles[i]}%'
                """
            for i in range(1, len(fuzzed_names)):
                other_names += f"""
                OR Actor.actorName LIKE '%{fuzzed_names[i]}%'
                """
            query += f"""
            WHERE (Movie.movieRating >= {minimum_rating})
                And (Actor.actorName LIKE '%{fuzzed_names[0]}%' {other_names})
                AND (Movie.movieTitle LIKE '%{fuzzed_titles[0]}%' {other_titles})
            """
            print(query)

        if genre_name == "all":
            query += ""
        else:
            query += f"AND Genre.genreName LIKE '%{genre_name}%'"

        if sort_by == "Rating (Ascending)":
            query += f"ORDER BY Movie.movieRating ASC"
        elif sort_by == "Rating (Descending)":
            query += f"ORDER BY Movie.movieRating DESC"
        elif sort_by == "Year Released (Ascending)":
            query += f"ORDER BY Movie.yearReleased ASC"
        elif sort_by == "Year Released (Descending)":
            query += f"ORDER BY Movie.yearReleased DESC"
        elif sort_by == "Runtime (Ascending)":
            query += f"ORDER BY Movie.runtime ASC"
        elif sort_by == "Runtime (Descending)":
            query += f"ORDER BY Movie.runtime DESC"
        elif sort_by == "none":
            query += ""

        movies = db.execute(query).fetchall()
        moviechunks = split_moviechunks(movies, N, ROW_LIMIT)
        moreLeft = N * ROW_LIMIT < len(movies)

        db.close()
        return render_template('search.html', moviechunks=moviechunks, moreLeft=moreLeft, genre_names=genre_names, sort_by_fields=sort_by_fields, title=title, actor=actor_name, genre=genre_name, sort_by=sort_by,  user=current_user)
    else:
        genre_name = request.form.get("genre")
        query = f"""
        SELECT DISTINCT Movie.movieTitle, Movie.movieRating, Movie.yearReleased, Movie.runtime, Movie.posterImgLink, Movie.movieID,
        Watched.likes, (SELECT COUNT(*) FROM Watched WHERE Movie.movieID = Watched.movieID AND Watched.userID = '{current_user.id}') AS watch
        FROM Movie
        LEFT JOIN Watched ON Movie.movieID = Watched.movieID AND Watched.userID = '{current_user.id}';
        """
        movies = db.execute(query).fetchall()
        moviechunks = split_moviechunks(movies, N, ROW_LIMIT)
        moreLeft = N * ROW_LIMIT < len(movies)

        db.close()
        return render_template('search.html', moviechunks=moviechunks, moreLeft=moreLeft, genre_names=genre_names,
                               sort_by_fields=sort_by_fields, user=current_user)


@views.route('/profile', methods=["GET", "POST"])
@login_required
def profile():
    db = DB()

    is_search = False
    is_genre = False
    is_actor = False

    aName = ""

    if request.method == "POST":
        follow = request.form.get("Follow")
        unfollow = request.form.get("Unfollow")

        first = request.form.get("first")
        last = request.form.get("last")

        addGenre = request.form.get("addGenre")
        removeGenre = request.form.get("removeGenre")

        addActor = request.form.get("addActor")
        removeActor = request.form.get("removeActor")

        actor = request.form.get("aName")

        print(request.form)

        if first is not None:
            firstName = first
            is_search = True

        if last is not None:
            lastName = last
            is_search = True

        if actor is not None:
            aName = actor
            is_actor = True

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

        if addGenre is not None:
            select_query = f"""
            SELECT * FROM FavGenre WHERE userID = '{current_user.id}' AND genreID = '{addGenre}'
            """
            val = db.execute(select_query).fetchall()

            if len(val) == 0:
                is_genre = True
                add_genre_query = f"""
                INSERT INTO FavGenre (userID, genreID)
                VALUES ('{current_user.id}', '{addGenre}');
                """
                db.execute(add_genre_query).fetchall()
                db.commit()

        if removeGenre is not None:
            is_genre = True
            remove_genre_query = f"""
            DELETE FROM FavGenre
            WHERE userID = '{current_user.id}'
                AND genreID = '{removeGenre}';
            """
            db.execute(remove_genre_query).fetchall()
            db.commit()

        if addActor is not None:
            is_actor = True
            select_query = f"""
            SELECT * FROM FavActor WHERE userID = '{current_user.id}' AND actorID = '{addActor}'
            """
            val = db.execute(select_query).fetchall()

            if len(val) == 0:
                add_actor_query = f"""
                INSERT INTO FavActor (userID, actorID)
                VALUES ('{current_user.id}', '{addActor}');
                """
                db.execute(add_actor_query).fetchall()
                db.commit()

        if removeActor is not None:
            is_actor = True
            remove_actor_query = f"""
            DELETE FROM FavActor
            WHERE userID = '{current_user.id}'
                AND actorID = '{removeActor}';
            """
            db.execute(remove_actor_query).fetchall()
            db.commit()

    fav_actors_query = f"""
    SELECT F.actorID, A.actorName
    FROM FavActor F
    JOIN Actor A ON F.actorID == A.actorID
    WHERE F.userID = '{current_user.id}'
    ORDER BY A.actorName
    """
    fav_actors = db.execute(fav_actors_query).fetchall()

    genres_query = f"""
    SELECT genreID, genreName, (SELECT COUNT(*) 
        FROM FavGenre F 
        WHERE G.genreID = F.genreID AND F.userID = '{current_user.id}'
    )
    AS fav
    FROM Genre G
    """
    genres = db.execute(genres_query).fetchall()

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
    WHERE level > 0
    LIMIT 48;
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
        LIMIT 48;
        """
        search_results = db.execute(search_query).fetchall()
    else:
        firstName = ""
        lastName = ""
        search_results = None

    actor_query = f"""
    SELECT actorID, actorName
    FROM Actor
    WHERE actorName LIKE '%{aName}%' AND actorID NOT IN (SELECT actorID FROM FavActor WHERE userID = '{current_user.id}')
    ORDER BY actorName
    LIMIT 48;
    """
    actors = db.execute(actor_query).fetchall()

    db.close()

    return render_template(
        'profile.html', 
        user=current_user, 
        user_info=user_info, 
        fav_actors=fav_actors, 
        genres=genres, 
        following=following, 
        followers=followers, 
        suggested=suggested, 
        is_search=is_search, 
        is_genre=is_genre,
        is_actor=is_actor,
        search_results=search_results, 
        firstName=firstName, 
        lastName=lastName,
        aName=aName,
        actors=actors
    )


@views.route('/recommend', methods=["GET", "POST"])
@login_required
def recommend():
    db = DB()
    print(current_user.id)
    random_movies_query = f"""
    SELECT Movie.movieTitle, Movie.movieRating, Movie.yearReleased, Movie.runtime, Movie.posterImgLink
    FROM Movie
    WHERE Movie.movieID NOT IN (
        SELECT Watched.movieID
        FROM Watched
        WHERE Watched.userID = '{current_user.id}'
    )
    ORDER BY RANDOM()
    LIMIT 10;
    """
    random_movies = db.execute(random_movies_query).fetchall()

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

    rec_prev_liked_query = f"""
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
    rec_prev_liked = db.execute(rec_prev_liked_query).fetchall()

    follow_liked_query = f"""
    SELECT Movie.movieTitle, Movie.movieRating, Movie.yearReleased, Movie.runtime, Movie.posterImgLink
    FROM User
    JOIN Follows ON User.username = Follows.userID1
    JOIN Watched ON Follows.userID2 = Watched.userID
    JOIN Movie ON Watched.movieID = Movie.movieID
    WHERE User.username = '{current_user.id}'
    ORDER BY Watched.lastWatched DESC
    LIMIT 10;
    """
    follow_liked = db.execute(follow_liked_query).fetchall()

    from_faves_query = f"""
    SELECT Movie.movieTitle, Movie.movieRating, Movie.yearReleased, Movie.runtime, Movie.posterImgLink,
    (COUNT(DISTINCT Genre.genreID) + COUNT(DISTINCT Actor.actorID)) AS recommendScore
    FROM Movie
    JOIN MovieGenre ON Movie.movieID = MovieGenre.movieID
    JOIN Genre ON MovieGenre.genreID = Genre.genreID
    JOIN Starred ON Movie.movieID = Starred.movieID
    JOIN Actor ON Starred.actorID = Actor.actorID
    JOIN FavGenre ON Genre.genreID = FavGenre.genreID 
        AND FavGenre.userID = '{current_user.id}'
    JOIN FavActor ON Actor.actorID = FavActor.actorID 
        AND FavActor.userID = '{current_user.id}'
    WHERE Movie.movieID NOT IN (
        SELECT Watched.movieID
        FROM Watched
        WHERE Watched.userID = '{current_user.id}'
    )
    GROUP BY Movie.movieID, Movie.movieTitle
    ORDER BY recommendScore DESC
    LIMIT 10
    """
    rec_from_faves = db.execute(from_faves_query).fetchall()

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
        return render_template('recommend.html', again_movies=again_movies, rec_prev_liked=rec_prev_liked,
                               follow_liked=follow_liked, rec_from_faves=rec_from_faves, following=following,
                               rec_two=rec_two, random_movies = random_movies,
                               second_user=second_user, user=current_user, firstClicked=True)
    else:
        db.close()
        return render_template('recommend.html', again_movies=again_movies, rec_prev_liked=rec_prev_liked,
                               follow_liked=follow_liked, rec_from_faves=rec_from_faves, random_movies=random_movies,
                               following=following, user=current_user, firstClicked=False)
