import sys
import os
sys.path.append( '.' )
sys.path.append( '../production_dataset' )

from production_dataset.use_prod_dataset_util import load_csv_to_sql
from production_dataset.prod_dataset_consts import *

def load_prod_dataset(connection):
    with open('schema.sql') as f:
        connection.executescript(f.read())

    csv_files = [MOVIE_FILENAME, GENRE_FILENAME, MOVIEGENRE_FILENAME, ACTOR_FILENAME, STARRED_FILENAME, ROLE_FILENAME,
                 USER_FILENAME, FOLLOWS_FILENAME, FAVACTOR_FILENAME, FAVGENRE_FILENAME, WATCHED_FILENAME]
    insert_strings = ["Movie (movieID, movieTitle, movieRating, runtime, yearReleased, posterImgLink) VALUES (?, ?, ?, ?, ?, ?)",
                    "Genre (genreID, genreName) VALUES (?, ?)",
                    "MovieGenre (movieID, genreID) VALUES (?, ?)",
                    "Actor (actorID, actorName) VALUES (?, ?)",
                    "Starred (movieID, actorID) VALUES (?, ?)",
                    "ActorRole (movieID, actorID, roleName) VALUES (?, ?, ?)",
                    "User (username, firstName, lastName, userPassword, profilePicLink) VALUES (?, ?, ?, ?, ?)",
                    "Follows (userID1, userID2) VALUES (?, ?)",
                    "FavActor (userID, actorID) VALUES (?, ?)",
                    "FavGenre (userID, genreID) VALUES (?, ?)",
                    "Watched (userID, movieID, lastWatched, likes) VALUES (?, ?, ?, ?)"
                    ]

    for i in range(len(csv_files)):
        load_csv_to_sql(connection=connection, csv_filename="production_dataset/"+csv_files[i], insert_string=insert_strings[i])