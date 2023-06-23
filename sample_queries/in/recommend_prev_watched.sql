SELECT DISTINCT Movie.movieID, Movie.movieTitle
FROM Movie
JOIN MovieGenre ON Movie.movieID = MovieGenre.movieID
JOIN Genre ON MovieGenre.genreID = Genre.genreID
JOIN Starred ON Movie.movieID = Starred.movieID
JOIN Actor ON Starred.actorID = Actor.actorID
WHERE Movie.movieID NOT IN (
    SELECT Watched.movieID
    FROM Watched
    WHERE Watched.userID = 'frankvanvleet88'
)
AND (Genre.genreID IN (
        SELECT MovieGenre.genreID
        FROM MovieGenre
        WHERE MovieGenre.movieID IN (
            SELECT Watched.movieID
            FROM Watched
            WHERE Watched.userID = 'frankvanvleet88' AND Watched.likes = 1
        )
    )
    OR Actor.actorID IN (
        SELECT Starred.actorID
        FROM Starred
        WHERE Starred.movieID IN (
            SELECT Watched.movieID
            FROM Watched
            WHERE Watched.userID = 'frankvanvleet88' AND Watched.likes = 1
        )
    )
)
ORDER BY Movie.movieID DESC
LIMIT 5;