SELECT Movie.movieID, Movie.movieTitle
FROM Movie
WHERE Movie.movieID NOT IN (
    SELECT Watched.movieID
    FROM Watched
    WHERE Watched.userID = 'frankvanvleet88'
)
ORDER BY RANDOM();