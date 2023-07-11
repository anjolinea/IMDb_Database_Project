SELECT Watched.userID AS followed_username, Movie.movieTitle AS last_watched_movie
FROM User
JOIN Follows ON User.username = Follows.userID1
JOIN Watched ON Follows.userID2 = Watched.userID
JOIN Movie ON Watched.movieID = Movie.movieID
WHERE User.username = 'frankvanvleet40'
ORDER BY Watched.lastWatched DESC
LIMIT 5;