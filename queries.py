
# FOLLOWING IS NOW FOLLOW

f"""
SELECT DISTINCT Movie.movieTitle
FROM Movie
JOIN Starred ON Movie.movieID = Starred.movieID
JOIN Actor ON Starred.actorID = Actor.actorID
JOIN MovieGenre ON Movie.movieID = MovieGenre.movieID
JOIN Genre ON MovieGenre.genreID = Genre.genreID
WHERE Actor.actorName LIKE '{actor_name}'
    AND Genre.genreName LIKE '{genre_name}'
    AND Movie.movieRating >= minimum_rating;
"""

f"""
SELECT Movie.movieID, Movie.movieTitle
FROM Movie
WHERE Movie.movieID NOT IN (
    SELECT Watched.movieID
    FROM Watched
    WHERE Watched.userID = '{user_name}'
)
ORDER BY RANDOM();
"""

f"""
SELECT Movie.movieID, Movie.movieTitle,
    (COUNT(DISTINCT Genre.genreID) + COUNT(DISTINCT Actor.actorID)) AS recommendScore
FROM Movie
JOIN MovieGenre ON Movie.movieID = MovieGenre.movieID
JOIN Genre ON MovieGenre.genreID = Genre.genreID
JOIN Starred ON Movie.movieID = Starred.movieID
JOIN Actor ON Starred.actorID = Actor.actorID
JOIN FavGenre ON Genre.genreID = FavGenre.genreID 
    AND FavGenre.userID = '{user_name}'
JOIN FavActor ON Actor.actorID = FavActor.actorID 
    AND FavActor.userID = '{user_name}'
WHERE Movie.movieID NOT IN (
    SELECT Watched.movieID
    FROM Watched
    WHERE Watched.userID = '{user_name}'
)
GROUP BY Movie.movieID, Movie.movieTitle
ORDER BY recommendScore DESC
LIMIT {num_movies};
"""

f"""
SELECT DISTINCT Movie.movieID, Movie.movieTitle
FROM Movie
JOIN MovieGenre ON Movie.movieID = MovieGenre.movieID
JOIN Genre ON MovieGenre.genreID = Genre.genreID
JOIN Starred ON Movie.movieID = Starred.movieID
JOIN Actor ON Starred.actorID = Actor.actorID
WHERE Movie.movieID NOT IN (
    SELECT Watched.movieID
    FROM Watched
    WHERE Watched.userID = '{user_name}'
)
AND (Genre.genreID IN (
        SELECT MovieGenre.genreID
        FROM MovieGenre
        WHERE MovieGenre.movieID IN (
            SELECT Watched.movieID
            FROM Watched
            WHERE Watched.userID = '{user_name}' AND Watched.likes = 1
        )
    )
    OR Actor.actorID IN (
        SELECT Starred.actorID
        FROM Starred
        WHERE Starred.movieID IN (
            SELECT Watched.movieID
            FROM Watched
            WHERE Watched.userID = '{user_name}' AND Watched.likes = 1
        )
    )
)
ORDER BY Movie.movieID DESC
LIMIT {num_movies};
"""

## This query has error
f"""
SELECT Movie.movieID, Movie.movieTitle
FROM Movie
JOIN Watched ON Movie.movieID = Watched.movieID
WHERE Watched.userID = '{user_name}'
  AND Watched.likes = 1
  AND Watched.dateWatched <= DATE_SUB(CURRENT_DATE, INTERVAL 30 DAY)
ORDER BY Watched.dateWatched ASC
LIMIT {num_movies};
"""
## Stopped testing after this one ^

f"""
SELECT User.username AS followed_username, Movie.movieTitle AS last_watched_movie
FROM User
JOIN Following ON User.username = Following.userID1
JOIN Watched ON Following.userID2 = Watched.userID
JOIN Movie ON Watched.movieID = Movie.movieID
WHERE User.username = '{user_name}'
ORDER BY Watched.dateWatched DESC
LIMIT {num_movies};
"""

f"""
SELECT DISTINCT Movie.movieID, Movie.movieTitle
FROM Movie
JOIN MovieGenre ON Movie.movieID = MovieGenre.movieID
JOIN Genre ON MovieGenre.genreID = Genre.genreID
JOIN Starred ON Movie.movieID = Starred.movieID
JOIN Actor ON Starred.actorID = Actor.actorID
WHERE Movie.movieID NOT IN (
    SELECT Watched.movieID
    FROM Watched
    WHERE Watched.userID = '{user_name_1}'
)
AND Movie.movieID NOT IN (
    SELECT Watched.movieID
    FROM Watched
    WHERE Watched.userID = '{user_name_2}'
)
AND (
    Genre.genreID IN (
        SELECT FavGenre.genreID
        FROM FavGenre
        WHERE FavGenre.userID = '{user_name_1}'
    )
    OR Genre.genreID IN (
        SELECT FavGenre.genreID
        FROM FavGenre
        WHERE FavGenre.userID = '{user_name_2}'
    )
    OR Actor.actorID IN (
        SELECT FavActor.actorID
        FROM FavActor
        WHERE FavActor.userID = '{user_name_1}'
    )
    OR Actor.actorID IN (
        SELECT FavActor.actorID
        FROM FavActor
        WHERE FavActor.userID = '{user_name_2}'
    )
)
ORDER BY RAND()
LIMIT {num_movies};
"""

f"""
WITH RECURSIVE FollowersRecursive AS (
    SELECT Following.userID1 AS follower,
        Following.userID2 AS follower_of_follower, 
        0 AS level
    FROM Following
    WHERE Following.userID1 = '{user_name}'
    UNION ALL
    SELECT FollowersRecursive.follower,
        Following.userID2, 
        FollowersRecursive.level + 1
    FROM Following
    JOIN FollowersRecursive ON 
        Following.userID1 = FollowersRecursive.follower_of_follower
    WHERE FollowersRecursive.level < 2
)
SELECT follower_of_follower AS follower, MIN(level) AS level
FROM FollowersRecursive
GROUP BY follower_of_follower;
"""

f"""
INSERT INTO Watched (userID, movieID, dateWatched, likes)
VALUES ('username_of_user', 'movieID_of_new_movie', CURRENT_DATE, 0);
"""

f"""
DELETE FROM Watched
WHERE userID = 'username_of_user'
  AND movieID = 'movieID_of_movie_to_remove';
"""

f"""
INSERT INTO FavGenre (userID, genreID)
VALUES ('username_of_user', 'genreID_to_add');
"""

f"""
DELETE FROM FavGenre
WHERE userID = 'username_of_user' AND genreID = 'genreID_to_remove';
"""

f"""
INSERT INTO FavActor (userID, actorID)
VALUES ('username_of_user', 'actorID_to_add');
"""

f"""
DELETE FROM FavActor
WHERE userID = 'username_of_user' AND actorID = 'actorID_to_remove';
"""

f"""
UPDATE Watched
SET likes = 'new_likes_value'
WHERE userID = 'username_of_user' AND movieID = 'movieID_to_update';
"""

f"""
UPDATE User
SET password = 'new_password'
WHERE username = 'username_of_user';
"""

f"""
SELECT COUNT(*) AS count
FROM User
WHERE username = 'entered_username' AND password = 'entered_password';
"""