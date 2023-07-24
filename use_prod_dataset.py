import sqlite3
import sys
import os
sys.path.append( '.' )
sys.path.append( '../production_dataset' )

from production_dataset.use_prod_dataset_util import *
from load_prod_dataset import load_prod_dataset

connection = sqlite3.connect('prod_database.db')
#load_prod_dataset(connection)

# --- for playing around with SQL files -----
def test_SQL_query(test_name):
    test_name = "recommend_fav_genre_actor"

    in_query_folder = "production_sample_queries/in/"
    in_query_file = test_name + ".sql"
    in_file = in_query_folder + in_query_file

    out_query_folder = "production_sample_queries/out/"
    out_query_file = test_name + ".out"
    out_file = out_query_folder + out_query_file

    end = run_command_from_file(connection=connection, input_filename=in_file, output_filename=out_file, printOutput=False)
    return end

N = 100
def latency(test_name):
    return sum([test_SQL_query(test_name) for i in range(N)]) / N

def test_index():
    for test_name in ["connections", "recommend_fav_genre_actor", "recommend_from_follower", "recommend_new_for_two", "recommend_prev_watched", "recommend_rewatch", "search_movie_on_criteria", "select_new_movies"]:
        for schema in ["schema.sql", "orig-schema.sql"]:
                load_prod_dataset(connection, schema)
                print(test_name + " " + schema + ": " + '{:.6f}s on average for the query'.format(latency(test_name)))
                if schema == "orig-schema.sql":
                    print(test_name + " difference in time between schemas" + ": " + '{:.6f}s on average for the query'.format(schema_sql_latency - latency(test_name)))
                else:
                    schema_sql_latency = latency(test_name)

# print('{:.6f}s on average for the query'.format(latency))
# ------------------

test_index()

load_prod_dataset(connection, "orig-schema.sql")
query = """
EXPLAIN QUERY PLAN
SELECT DISTINCT Movie.movieTitle, Movie.movieRating, Movie.yearReleased, Movie.runtime
FROM Movie
JOIN Starred ON Movie.movieID = Starred.movieID
JOIN Actor ON Starred.actorID = Actor.actorID
JOIN MovieGenre ON Movie.movieID = MovieGenre.movieID
JOIN Genre ON MovieGenre.genreID = Genre.genreID
WHERE Actor.actorName LIKE '%Z%'
    AND Genre.genreName LIKE '%Action%'
    AND Movie.movieTitle LIKE '%'
    AND Movie.movieRating >= 5
LIMIT 10;
"""

## a CHECK constraint violation should happen!
#run_command_from_string(connection, query, True)