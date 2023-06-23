-- insert, delete queries

INSERT INTO Watched (userID, movieID, dateWatched, likes)
VALUES ('username_of_user', 'movieID_of_new_movie', CURRENT_DATE, 0);

DELETE FROM Watched
WHERE userID = 'username_of_user'
  AND movieID = 'movieID_of_movie_to_remove';

INSERT INTO FavGenre (userID, genreID)
VALUES ('username_of_user', 'genreID_to_add');

DELETE FROM FavGenre
WHERE userID = 'username_of_user' AND genreID = 'genreID_to_remove';

INSERT INTO FavActor (userID, actorID)
VALUES ('username_of_user', 'actorID_to_add');

DELETE FROM FavActor
WHERE userID = 'username_of_user' AND actorID = 'actorID_to_remove';

UPDATE Watched
SET likes = 'new_likes_value'
WHERE userID = 'username_of_user' AND movieID = 'movieID_to_update';

UPDATE User
SET password = 'new_password'
WHERE username = 'username_of_user';

SELECT COUNT(*) AS count
FROM User
WHERE username = 'entered_username' AND password = 'entered_password';
