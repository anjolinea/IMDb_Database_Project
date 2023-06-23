SELECT Movie.movieID, Movie.movieTitle
FROM Movie
JOIN Watched ON Movie.movieID = Watched.movieID
WHERE Watched.userID = 'frankvanvleet88'
  AND Watched.likes = 1
  AND Watched.dateWatched <= DATETIME(CURRENT_DATE, '-30 day')
ORDER BY Watched.dateWatched ASC
LIMIT 5;