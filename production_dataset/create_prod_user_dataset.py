import pandas as pd
import random
import string
from datetime import date, timedelta
from prod_dataset_consts import *

actors_df = pd.read_csv(ACTOR_FILENAME)
genres_df = pd.read_csv(GENRE_FILENAME)
movies_df = pd.read_csv(MOVIE_FILENAME)

def get_random_string(length):
    # choose from all lowercase letter
    letters = string.ascii_letters
    result_str = ''.join(random.choice(letters) for i in range(length))
    return(result_str)

def load_names_into_set(filename):
    names = set()
    with open(filename) as fhand:
        for row in fhand:
            names.add(row.split(" ")[0].lower())
    return names

# SET SEED
random.seed(20880034)

# Users Table
users_df = pd.DataFrame({'username': pd.Series(dtype='str'),
                         'firstName' : pd.Series(dtype='str'),
                         'lastName' : pd.Series(dtype="str"),
                         'password' : pd.Series(dtype='str')})

# hardcoded first, last names
firstnames = load_names_into_set(FIRSTNAME_FILENAME)
lastnames = load_names_into_set(LASTNAME_FILENAME)
usernames = []

for fn in firstnames:
    for ln in lastnames:
        # Define the new row to be added
        username = fn + ln + "{:02d}".format(int(random.random() * 100))
        usernames.append(username)

        # TODO: change to hashing
        password = get_random_string(10)
        fn_db = fn.capitalize()
        ln_db = ln.capitalize()

        new_row = {'username': username, 'firstName': fn_db, 'lastName': ln_db, 'password' : password}
        
        # Use the loc method to add the new row to the DataFrame
        users_df.loc[len(users_df)] = new_row

## Follow table
follows_df = pd.DataFrame({'userID1': pd.Series(dtype='str'),
                           'userID2' : pd.Series(dtype='str')})


# make followings
followings = []
num_of_following_pairs = 17500
num_of_friend_pairs = 1250

for i in range(num_of_following_pairs):
    while True:
        f1 = random.choice(usernames)
        f2 = random.choice(usernames)
        if f1 != f2 and (f1, f2) not in followings:
            followings.append((f1, f2))
            break

for i in range(num_of_friend_pairs):
    while True:
        f1 = random.choice(usernames)
        f2 = random.choice(usernames)
        if f1 != f2 and (f1, f2) not in followings and (f2, f1) not in followings:
            followings.append((f1, f2))
            followings.append((f2, f1))
            break

follows_df = pd.DataFrame(followings, columns=['follower', 'following'])

# FavActors
actors = actors_df["actorID"].to_list()
fav_actors = []
num_of_fav_actors = 15000
for i in range(num_of_fav_actors):
    while True:
        u = random.choice(usernames)
        a = random.choice(actors)
        if (u, a) not in fav_actors:
            fav_actors.append((u,a))
            break

favActors_df = pd.DataFrame(fav_actors, columns=['userID', 'actorID'])

# FavGenre
genres = genres_df["genreID"].to_list()
fav_genres = []
num_of_fav_genres = 5000
for i in range(num_of_fav_genres):
    while True:
        u = random.choice(usernames)
        g = random.choice(genres)
        if (u, g) not in fav_genres:
            fav_genres.append((u,g))
            break

favGenres_df = pd.DataFrame(fav_genres, columns=['userID', 'genreID'])

# Watched
start_dt = date(2000, 1, 1)
end_dt = date(2023, 6, 21)
delta = timedelta(days=1)
dates = []
while start_dt <= end_dt:
    dates.append(start_dt.isoformat())
    start_dt += delta

movies = movies_df["movieID"].to_list()

watched = []
num_of_watched = 10000
for i in range(num_of_watched):
    liked = random.randint(0, 1)
    last_watched = random.choice(dates)
    movie = random.choice(movies)
    username = random.choice(usernames)

    if (username, movie) not in [(w[0], w[1]) for w in watched]:
        watched.append((username, movie, last_watched, liked))

watched_df = pd.DataFrame(watched, columns=['userID', 'movieID', 'lastWatched', 'likes'])

# upload tables to CSV files
users_df.to_csv(USER_FILENAME, index=False)
follows_df.to_csv(FOLLOWS_FILENAME, index=False)
favGenres_df.to_csv(FAVGENRE_FILENAME, index=False)
favActors_df.to_csv(FAVACTOR_FILENAME, index=False)
watched_df.to_csv(WATCHED_FILENAME, index=False)

