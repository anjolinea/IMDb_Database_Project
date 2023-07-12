-- Search Movie based on Criteria
SELECT DISTINCT Movie.movieTitle, Movie.movieRating, Movie.yearReleased, Movie.runtime
FROM Movie
JOIN Starred ON Movie.movieID = Starred.movieID
JOIN Actor ON Starred.actorID = Actor.actorID
JOIN MovieGenre ON Movie.movieID = MovieGenre.movieID
JOIN Genre ON MovieGenre.genreID = Genre.genreID
WHERE Actor.actorName LIKE '%Z%'
    AND Genre.genreName LIKE '%Action%'
    AND Movie.movieTitle LIKE '%'
    AND Movie.movieRating >= 5
LIMIT 10;


-- Recommend New Movie
SELECT Movie.movieID, Movie.movieTitle
FROM Movie
WHERE Movie.movieID NOT IN (
    SELECT Watched.movieID
    FROM Watched
    WHERE Watched.userID = 'jenniferhernandez64'
)
ORDER BY RANDOM()
LIMIT 10;

-- Find Connections
WITH RECURSIVE FollowersRecursive AS (
    SELECT Follows.userID1 AS follower,
        Follows.userID2 AS follower_of_follower, 
        0 AS level
    FROM Follows
    WHERE Follows.userID1 = 'jenniferhernandez64'
    UNION ALL
    SELECT FollowersRecursive.follower,
        Follows.userID2, 
        FollowersRecursive.level + 1
    FROM Follows
    JOIN FollowersRecursive ON 
        Follows.userID1 = FollowersRecursive.follower_of_follower
    WHERE FollowersRecursive.level < 2
)
SELECT follower_of_follower AS follower, MIN(level) AS level
FROM FollowersRecursive
GROUP BY follower_of_follower
LIMIT 10;

-- Recommend Movie based on Favourites
SELECT Movie.movieID, Movie.movieTitle,
    (COUNT(DISTINCT Genre.genreID) + COUNT(DISTINCT Actor.actorID)) AS recommendScore
FROM Movie
JOIN MovieGenre ON Movie.movieID = MovieGenre.movieID
JOIN Genre ON MovieGenre.genreID = Genre.genreID
JOIN Starred ON Movie.movieID = Starred.movieID
JOIN Actor ON Starred.actorID = Actor.actorID
JOIN FavGenre ON Genre.genreID = FavGenre.genreID 
    AND FavGenre.userID = 'jenniferhernandez64'
JOIN FavActor ON Actor.actorID = FavActor.actorID 
    AND FavActor.userID = 'jenniferhernandez64'
WHERE Movie.movieID NOT IN (
    SELECT Watched.movieID
    FROM Watched
    WHERE Watched.userID = 'jenniferhernandez64'
)
GROUP BY Movie.movieID, Movie.movieTitle
ORDER BY recommendScore DESC
LIMIT 10;

-- Recommend for Two
SELECT DISTINCT Movie.movieID, Movie.movieTitle
FROM Movie
JOIN MovieGenre ON Movie.movieID = MovieGenre.movieID
JOIN Genre ON MovieGenre.genreID = Genre.genreID
JOIN Starred ON Movie.movieID = Starred.movieID
JOIN Actor ON Starred.actorID = Actor.actorID
WHERE Movie.movieID NOT IN (
    SELECT Watched.movieID
    FROM Watched
    WHERE Watched.userID = 'jenniferhernandez64'
)
AND Movie.movieID NOT IN (
    SELECT Watched.movieID
    FROM Watched
    WHERE Watched.userID = 'wayneward04'
)
AND (
    Genre.genreID IN (
        SELECT FavGenre.genreID
        FROM FavGenre
        WHERE FavGenre.userID = 'jenniferhernandez64'
    )
    OR Genre.genreID IN (
        SELECT FavGenre.genreID
        FROM FavGenre
        WHERE FavGenre.userID = 'wayneward04'
    )
    OR Actor.actorID IN (
        SELECT FavActor.actorID
        FROM FavActor
        WHERE FavActor.userID = 'jenniferhernandez64'
    )
    OR Actor.actorID IN (
        SELECT FavActor.actorID
        FROM FavActor
        WHERE FavActor.userID = 'wayneward04'
    )
)
ORDER BY RANDOM()
LIMIT 10;
