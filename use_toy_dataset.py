import sqlite3
import sys
import os
sys.path.append( '.' )
sys.path.append( '../toy_dataset' )

from toy_dataset.use_toy_dataset_util import *
from load_toy_dataset import load_toy_dataset

connection = sqlite3.connect('toy_database.db')
load_toy_dataset(connection)

# # --- for playing around with SQL files -----
# test_name = "recommend_rewatch"

# in_query_folder = "toy_sample_queries/in/"
# in_query_file = test_name + ".sql"
# in_file = in_query_folder + in_query_file

# out_query_folder = "toy_sample_queries/out/"
# out_query_file = test_name + ".out"
# out_file = out_query_folder + out_query_file

# run_command_from_file(connection=connection, input_filename=in_file, output_filename=out_file)
# # ------------------

query = """
SELECT * FROM USER
"""
run_command_from_string(connection, query, True)