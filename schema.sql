DROP TABLE IF EXISTS Movie;
DROP TABLE IF EXISTS MovieGenre;
DROP TABLE IF EXISTS Genre;
DROP TABLE IF EXISTS Starred;
DROP TABLE IF EXISTS Actor;
DROP TABLE IF EXISTS ActorRole;
DROP TABLE IF EXISTS User;
DROP TABLE IF EXISTS Follow;
DROP TABLE IF EXISTS FavActor;
DROP TABLE IF EXISTS FavGenre;
DROP TABLE IF EXISTS Watched;

CREATE TABLE Movie (
    movieID VARCHAR(15) NOT NULL PRIMARY KEY,
    movieTitle TEXT NOT NULL,
    yearReleased INT NOT NULL,
    runtimeMinutes INT NOT NULL,
    movieRating FLOAT NOT NULL
);

CREATE TABLE Genre (
    genreName VARCHAR(50) NOT NULL,
    genreID VARCHAR(3) NOT NULL PRIMARY KEY
);

CREATE TABLE MovieGenre (
    movieID VARCHAR(15) NOT NULL REFERENCES Movie(movieID),
    genreID VARCHAR(3) NOT NULL REFERENCES Genre(genreID),
    PRIMARY KEY(movieID, genreID)
);

CREATE TABLE Actor (
    actorID VARCHAR(15) NOT NULL PRIMARY KEY,
    actorName VARCHAR(60) NOT NULL
);

CREATE TABLE Starred (
    movieID VARCHAR(15) NOT NULL REFERENCES Movie(movieID),
    actorID VARCHAR(15) NOT NULL REFERENCES Actor(actorID),
    PRIMARY KEY(movieID, actorID)
);

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
    userPassword VARCHAR(60) NOT NULL
);

CREATE TABLE Follow (
    userID1 VARCHAR(40) NOT NULL REFERENCES User(username),
    userID2 VARCHAR(40) NOT NULL REFERENCES User(username),
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
    dateWatched DATE,
    likes BIT,
    PRIMARY KEY(userID, movieID)
);
