import sqlite3
from use_toy_dataset_util import load_csv_to_sql

# LOAD ALL CSV FILES INTO SQL
USER_FILENAME = "data/users.csv"
FAVACTOR_FILENAME = "data/favactors.csv"
FAVGENRE_FILENAME = "data/favgenres.csv"
WATCHED_FILENAME = "data/watched.csv"
FOLLOWS_FILENAME = "data/follows.csv"
MOVIES_FILENAME = "data/movies.csv"
MOVIEGENRE_FILENAME = "data/moviegenre.csv"
GENRES_FILENAME = "data/genres.csv"
STARRED_FILENAME = "data/starred.csv"
ACTOR_FILENAME = "data/actors.csv"
ROLE_FILENAME = "data/roles.csv"

def load_toy_dataset(connection):
    with open('schema.sql') as f:
        connection.executescript(f.read())

    csv_files = [MOVIES_FILENAME, GENRES_FILENAME, MOVIEGENRE_FILENAME, ACTOR_FILENAME, STARRED_FILENAME, ROLE_FILENAME,
                 USER_FILENAME, FOLLOWS_FILENAME, FAVACTOR_FILENAME, FAVGENRE_FILENAME, WATCHED_FILENAME]
    insert_strings = ["Movie (movieID, movieTitle, yearReleased, runtimeMinutes, movieRating) VALUES (?, ?, ?, ?, ?)",
                    "Genre (genreName, genreID) VALUES (?, ?)",
                    "MovieGenre (movieID, genreID) VALUES (?, ?)",
                    "Actor (actorID, actorName) VALUES (?, ?)",
                    "Starred (movieID, actorID) VALUES (?, ?)",
                    "ActorRole (movieID, actorID, roleName) VALUES (?, ?, ?)",
                    "User (username, firstName, lastName, userPassword) VALUES (?, ?, ?, ?)",
                    "Follow (userID1, userID2) VALUES (?, ?)",
                    "FavActor (userID, actorID) VALUES (?, ?)",
                    "FavGenre (userID, genreID) VALUES (?, ?)",
                    "Watched (userID, movieID, dateWatched, likes) VALUES (?, ?, ?, ?)"
                    ]

    for i in range(len(csv_files)):
        load_csv_to_sql(connection=connection, csv_filename="toy_dataset/"+csv_files[i], insert_string=insert_strings[i])