SELECT Movie.movieID, Movie.movieTitle
FROM Movie
JOIN Watched ON Movie.movieID = Watched.movieID
WHERE Watched.userID = 'jenniferhernandez64'
  AND Watched.likes = 1
  AND Watched.lastWatched <= DATETIME(CURRENT_DATE, '-30 day')
ORDER BY Watched.lastWatched ASC
LIMIT 10;