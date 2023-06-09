import pandas as pd
import random
import string
from datetime import date, timedelta
from werkzeug.security import generate_password_hash
from toy_dataset_consts import *

actors_df = pd.read_csv(ACTOR_FILENAME)
genres_df = pd.read_csv(GENRE_FILENAME)
movies_df = pd.read_csv(MOVIE_FILENAME)

# requires length >= 5
def get_random_string(length):
    lowercase_letters = ''.join(random.choice(string.ascii_lowercase) for i in range(length-4))
    uppercase_letters = ''.join(random.choice(string.ascii_uppercase) for i in range(2))
    numbers = ''.join(str(random.choice(list(range(10)))) for i in range(2))
    
    s = lowercase_letters + uppercase_letters + numbers
    l = list(s)
    random.shuffle(l)
    result = ''.join(l)
    return(result)

# SET SEED
random.seed(20880034)

# Users Table
users_df = pd.DataFrame({'username': pd.Series(dtype='str'),
                         'firstName' : pd.Series(dtype='str'),
                         'lastName' : pd.Series(dtype="str"),
                         'userPassword' : pd.Series(dtype='str'),
                         'profilePicLink' : pd.Series(dtype='str')})

# hardcoded first, last names
firstnames = ["alice", "bob", "charlie", "dan", "eve", "frank"]
lastnames = ["vanvleet", "siakam", "watanabe", "barnes", "anunoby"]
usernames = []

for fn in firstnames:
    for ln in lastnames:
        # Define the new row to be added
        username = fn + ln + "{:02d}".format(int(random.random() * 100))
        usernames.append(username)

        password = generate_password_hash(get_random_string(10), method='scrypt')
        fn_db = fn.capitalize()
        ln_db = ln.capitalize()
        profile_link_db = DEFAULT_PROFILE_PIC_LINK

        new_row = {'username': username, 'firstName': fn_db, 'lastName': ln_db, 'userPassword' : password, 'profilePicLink' : profile_link_db}
        
        # Use the loc method to add the new row to the DataFrame
        users_df.loc[len(users_df)] = new_row

## Follow table
follows_df = pd.DataFrame({'userID1': pd.Series(dtype='str'),
                           'userID2' : pd.Series(dtype='str')})


# make followings
followings = []
num_of_following_pairs = 40
num_of_friend_pairs = 20

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
num_of_fav_actors = 60
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
num_of_fav_genres = 50
for i in range(num_of_fav_genres):
    while True:
        u = random.choice(usernames)
        g = random.choice(genres)
        if (u, g) not in fav_genres:
            fav_genres.append((u,g))
            break

favGenres_df = pd.DataFrame(fav_genres, columns=['userID', 'genreID'])

# Watched
start_dt = date(2021, 1, 1)
end_dt = date(2023, 6, 21)
delta = timedelta(days=1)
dates = []
while start_dt <= end_dt:
    dates.append(start_dt.isoformat())
    start_dt += delta

movies = movies_df["movieID"].to_list()

watched = []
num_of_watched = 130
for i in range(num_of_watched):
    liked = random.randint(0, 1)
    date_watched = random.choice(dates)
    movie = random.choice(movies)
    username = random.choice(usernames)

    if (username, movie) not in [(w[0], w[1]) for w in watched]:
        watched.append((username, movie, date_watched, liked))

watched_df = pd.DataFrame(watched, columns=['userID', 'movieID', 'lastWatched', 'likes'])

# upload tables to CSV files
users_df.to_csv(USER_FILENAME, index=False)
follows_df.to_csv(FOLLOWS_FILENAME, index=False)
favGenres_df.to_csv(FAVGENRE_FILENAME, index=False)
favActors_df.to_csv(FAVACTOR_FILENAME, index=False)
watched_df.to_csv(WATCHED_FILENAME, index=False)

