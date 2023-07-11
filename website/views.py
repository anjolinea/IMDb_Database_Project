from flask import Blueprint, render_template, request
from . import DB
from flask_login import login_required, current_user

views = Blueprint('views', __name__)

N = 4
ROW_LIMIT = 4

def split_moviechunks(movies, n, row_limit):
    return [movies[i * n:(i + 1) * n] for i in range((len(movies) + n - 1) // n )][:row_limit] 

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
        return render_template('search.html', isSearch=True, moviechunks=moviechunks, moreLeft=moreLeft, user=current_user)
    else:
        return render_template('search.html', isSearch=False, user=current_user)
    
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
    SELECT userID2 AS following, firstName, lastName, profilePicLink
    FROM Follows, User
    WHERE userID1 = '{current_user.id}' AND username = userID2
    """
    following = db.execute(following_query).fetchall()

    followers_query = f"""
    SELECT F1.userID1 AS follower, firstName, lastName, profilePicLink, (
        SELECT COUNT(*) FROM Follows F2 WHERE F2.userID2 = F1.userID1 AND F2.userID1 = F1.userID2
    ) AS isFollowing
    FROM Follows F1, User
    WHERE F1.userID2 = '{current_user.id}' AND username = F1.userID1
    """
    followers = db.execute(followers_query).fetchall()

    suggested_query = f"""
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
    ORDER BY level;
    """
    suggested = db.execute(suggested_query).fetchall()

    if is_search:
        search_query = f"""
        SELECT username, firstName, lastName, profilePicLink, (
           SELECT COUNT(*) FROM Follows WHERE userID1 = '{current_user.id}' AND userID2 = username
        ) AS isFollowing
        FROM User 
        WHERE firstName LIKE '%{firstName}%' AND lastName LIKE '%{lastName}%'
        """
        search_results = db.execute(search_query).fetchall()
    else:
        firstName = ""
        lastName = ""
        search_results = None

    db.close()

    return render_template('profile.html', user=current_user, following=following, followers=followers, suggested=suggested, is_search=is_search, search_results=search_results, firstName=firstName, lastName=lastName)
    
@views.route('/settings', methods=["GET", "POST"])
@login_required
def settings():
    return render_template('settings.html', user=current_user)