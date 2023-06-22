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
insert_strings = ["Movie (movieID, movieTitle, yearReleased, runtimeMinutes, movieRating) VALUES (?, ?, ?, ?, ?)",
                  "Genre (genreName, genreID) VALUES (?, ?)",
                  "MovieGenre (movieID, genreID) VALUES (?, ?)",
                  "Actor (actorID, actorName) VALUES (?, ?)",
                  "Starred (movieID, actorID) VALUES (?, ?)"]

for i in range(len(csv_files)):
    load_csv_to_sql(connection=connection, csv_filename="toy_dataset/"+csv_files[i], insert_string=insert_strings[i])

actor_name = "Tom Holland"
genre_name = "Action"
minimum_rating = 5

command = f"""
SELECT Movie.movieTitle
FROM Movie
JOIN Starred ON Movie.movieID = Starred.movieID
JOIN Actor ON Starred.actorID = Actor.actorID
JOIN MovieGenre ON Movie.movieID = MovieGenre.movieID
JOIN Genre ON MovieGenre.genreID = Genre.genreID
WHERE Actor.actorName = '{actor_name}'
    AND Genre.genreName = '{genre_name}'
    AND Movie.movieRating >= {minimum_rating};
"""
run_command_view_output(connection=connection, command=command)