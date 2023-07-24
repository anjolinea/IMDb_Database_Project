DROP TABLE IF EXISTS Movie;
DROP TABLE IF EXISTS MovieGenre;
DROP TABLE IF EXISTS Genre;
DROP TABLE IF EXISTS Starred;
DROP TABLE IF EXISTS Actor;
DROP TABLE IF EXISTS ActorRole;
DROP TABLE IF EXISTS User;
DROP TABLE IF EXISTS Follows;
DROP TABLE IF EXISTS FavActor;
DROP TABLE IF EXISTS FavGenre;
DROP TABLE IF EXISTS Watched;

CREATE TABLE Movie (
    movieID VARCHAR(15) NOT NULL PRIMARY KEY,
    movieTitle TEXT NOT NULL,
    movieRating FLOAT NOT NULL,
    runtime INT NOT NULL,
    yearReleased INT NOT NULL,
    posterImgLink VARCHAR(150)
);

CREATE INDEX MovieTitleIndex ON Movie(movieTitle);

CREATE TABLE Genre (
    genreID VARCHAR(3) NOT NULL PRIMARY KEY,
    genreName VARCHAR(50) NOT NULL
);

CREATE INDEX GenreNameIndex ON Genre(genreName);

CREATE TABLE MovieGenre (
    movieID VARCHAR(15) NOT NULL REFERENCES Movie(movieID),
    genreID VARCHAR(3) NOT NULL REFERENCES Genre(genreID),
    PRIMARY KEY(movieID, genreID)
);

CREATE TABLE Actor (
    actorID VARCHAR(15) NOT NULL PRIMARY KEY,
    actorName VARCHAR(60) NOT NULL
);

CREATE INDEX ActorNameIndex ON Actor(actorName);

CREATE TABLE Starred (
    movieID VARCHAR(15) NOT NULL REFERENCES Movie(movieID),
    actorID VARCHAR(15) NOT NULL REFERENCES Actor(actorID),
    PRIMARY KEY(movieID, actorID)
);

-- usually searching on actors' movies, not movies' actors
CREATE INDEX StarredIndex ON Starred(actorID, movieID);

CREATE TABLE ActorRole (
    movieID VARCHAR(15) NOT NULL,
    actorID VARCHAR(15) NOT NULL,
    roleName VARCHAR(60) NOT NULL,
    PRIMARY KEY(movieID, actorID, roleName),
    CONSTRAINT fk_starred foreign key (movieID, actorID) 
                          references Starred (movieID, actorID)
);

CREATE TABLE User (
    username VARCHAR(40) NOT NULL PRIMARY KEY,
    firstName VARCHAR(40) NOT NULL,
    lastName VARCHAR(40) NOT NULL,
    userPassword VARCHAR(200) NOT NULL,
    profilePicLink VARCHAR(150) NOT NULL
);

CREATE TABLE Follows (
    userID1 VARCHAR(40) NOT NULL REFERENCES User(username),
    userID2 VARCHAR(40) NOT NULL REFERENCES User(username) CHECK (userID1 <> userID2),
    PRIMARY KEY(userID1, userID2)
);

CREATE TABLE FavActor (
    userID VARCHAR(40) NOT NULL REFERENCES User(username),
    actorID VARCHAR(15) NOT NULL REFERENCES Actor(actorID),
    PRIMARY KEY(userID, actorID)
);

CREATE TABLE FavGenre (
    userID VARCHAR(40) NOT NULL REFERENCES User(username),
    genreID VARCHAR(3) NOT NULL REFERENCES Genre(genreID),
    PRIMARY KEY(userID, genreID)
);

CREATE TABLE Watched (
    userID VARCHAR(40) NOT NULL REFERENCES User(username),
    movieID VARCHAR(15) NOT NULL REFERENCES Movie(movieID),
    lastWatched DATE,
    likes BIT,
    PRIMARY KEY(userID, movieID)
);

--CREATE INDEX WatcheduserIDIndex ON Watched(userID);
--CREATE INDEX WatchedLastWatchedIndex ON Watched(lastWatched);