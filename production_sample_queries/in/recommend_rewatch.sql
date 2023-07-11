SELECT Movie.movieID, Movie.movieTitle
FROM Movie
JOIN Watched ON Movie.movieID = Watched.movieID
WHERE Watched.userID = 'frankvanvleet40'
  AND Watched.likes = 1
  AND Watched.lastWatched <= DATETIME(CURRENT_DATE, '-30 day')
ORDER BY Watched.lastWatched ASC
LIMIT 5;