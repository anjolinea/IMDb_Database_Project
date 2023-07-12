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