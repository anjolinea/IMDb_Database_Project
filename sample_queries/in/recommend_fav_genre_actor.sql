SELECT Movie.movieID, Movie.movieTitle,
    (COUNT(DISTINCT Genre.genreID) + COUNT(DISTINCT Actor.actorID)) AS recommendScore
FROM Movie
JOIN MovieGenre ON Movie.movieID = MovieGenre.movieID
JOIN Genre ON MovieGenre.genreID = Genre.genreID
JOIN Starred ON Movie.movieID = Starred.movieID
JOIN Actor ON Starred.actorID = Actor.actorID
JOIN FavGenre ON Genre.genreID = FavGenre.genreID 
    AND FavGenre.userID = 'frankvanvleet40'
JOIN FavActor ON Actor.actorID = FavActor.actorID 
    AND FavActor.userID = 'frankvanvleet40'
WHERE Movie.movieID NOT IN (
    SELECT Watched.movieID
    FROM Watched
    WHERE Watched.userID = 'frankvanvleet40'
)
GROUP BY Movie.movieID, Movie.movieTitle
ORDER BY recommendScore DESC
LIMIT 10