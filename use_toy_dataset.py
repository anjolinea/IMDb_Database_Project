import sqlite3
import sys
import os
sys.path.append( '.' )
sys.path.append( '../toy_dataset' )

from toy_dataset.use_toy_dataset_util import *
from load_toy_dataset import load_toy_dataset

connection = sqlite3.connect('database.db')
load_toy_dataset(connection)

actor_name = "%"
genre_name = "Action"
minimum_rating = 5
user_name_1 = "frankvanvleet88"
user_name_2 = "bobsiakam82"
user_name = "frankvanvleet88"
num_movies = 10

command = f"""
SELECT * FROM Watched
"""
run_command_view_output(connection=connection, command=command)