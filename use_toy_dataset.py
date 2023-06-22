from use_toy_dataset_util import *
from load_toy_dataset import load_toy_dataset
import sqlite3

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
WITH RECURSIVE FollowersRecursive AS (
    SELECT Follow.userID1 AS follower,
        Follow.userID2 AS follower_of_follower, 
        0 AS level
    FROM Follow
    WHERE Follow.userID1 = '{user_name}'
    UNION ALL
    SELECT FollowersRecursive.follower,
        Follow.userID2, 
        FollowersRecursive.level + 1
    FROM Follow
    JOIN FollowersRecursive ON 
        Follow.userID1 = FollowersRecursive.follower_of_follower
    WHERE FollowersRecursive.level < 2
)
SELECT follower_of_follower AS follower, MIN(level) AS level
FROM FollowersRecursive
GROUP BY follower_of_follower;
"""
run_command_view_output(connection=connection, command=command)