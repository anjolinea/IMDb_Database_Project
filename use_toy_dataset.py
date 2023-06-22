from use_toy_dataset_util import *
import sqlite3

connection = sqlite3.connect('database.db')

with open('schema.sql') as f:
    connection.executescript(f.read())

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

csv_files = [MOVIES_FILENAME, GENRES_FILENAME, MOVIEGENRE_FILENAME, ACTOR_FILENAME, STARRED_FILENAME]
insert_strings = ["Movie (movieID, movieTitle, yearReleased, runtimeMinutes, Rating) VALUES (?, ?, ?, ?, ?)",
                  "Genre (genreName, genreID) VALUES (?, ?)",
                  "MovieGenre (movieID, genreID) VALUES (?, ?)",
                  "Actor (actorID, actorName) VALUES (?, ?)",
                  "Starred (movieID, actorID) VALUES (?, ?)"]

for i in range(len(csv_files)):
    load_csv_to_sql(connection=connection, csv_filename="toy_dataset/"+csv_files[i], insert_string=insert_strings[i])

command = "SELECT * FROM Movie JOIN MovieGenre ON Movie.movieID = MovieGenre.movieID"
run_command_view_output(connection=connection, command=command)