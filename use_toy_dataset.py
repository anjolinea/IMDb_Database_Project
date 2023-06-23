import sqlite3
import sys
import os
sys.path.append( '.' )
sys.path.append( '../toy_dataset' )

from toy_dataset.use_toy_dataset_util import *
from load_toy_dataset import load_toy_dataset

test_name = "recommend_from_follower"

in_query_folder = "sample_queries/in/"
in_query_file = test_name + ".sql"
in_file = in_query_folder + in_query_file

out_query_folder = "sample_queries/out/"
out_query_file = test_name + ".out"
out_file = out_query_folder + out_query_file

connection = sqlite3.connect('database.db')
load_toy_dataset(connection)

run_command_from_file(connection=connection, input_filename=in_file, output_filename=out_file)