import sqlite3
import sys
import os
sys.path.append( '.' )
sys.path.append( '../' )
sys.path.append( '../production_dataset' )
sys.path.append( './production_dataset' )

from production_dataset.use_prod_dataset_util import *
from load_prod_dataset import load_prod_dataset

connection = sqlite3.connect('prod_database.db')
def test_SQL_query(test_name):
    in_query_folder = "production_sample_queries/in/"
    in_query_file = test_name + ".sql"
    in_file = in_query_folder + in_query_file

    out_query_folder = "production_sample_queries/out/"
    out_query_file = test_name + ".out"
    out_file = out_query_folder + out_query_file

    end = run_command_from_file(connection=connection, input_filename=in_file, output_filename=None, printOutput=False)
    return end

N = 100
def latency(test_name):
    return sum([test_SQL_query(test_name) for i in range(N)]) / N

def test_index():
    for test_name in ["connections", "recommend_fav_genre_actor", "recommend_from_follower", "recommend_new_for_two", "recommend_prev_watched", "recommend_rewatch", "search_movie_on_criteria", "select_new_movie"]:
        for schema in ["no-pk-index-schema.sql", "no-index-schema.sql", "indexed-schema.sql"]:
                load_prod_dataset(connection, "compare_schemas/" + schema)
                print(test_name + " " + schema + ": " + '{:.6f}s on average for the query'.format(latency(test_name)))

test_index()