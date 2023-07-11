## For adding custom data to the toy dataset so we can test it

import pandas as pd
from toy_dataset_consts import *
from werkzeug.security import generate_password_hash

# add custom person whose username we know
df = pd.read_csv(USER_FILENAME)
password = generate_password_hash("abcABC1234", method='scrypt')
new_row = {'username': 'ellenbelbeck', 'firstName': 'Ellen', 'lastName': 'Belbeck', 'userPassword' : password, 'profilePicLink' : DEFAULT_PROFILE_PIC_LINK}
df.loc[len(df)] = new_row
df.to_csv(USER_FILENAME, index=False)

# make custom person follow people
df = pd.read_csv(FOLLOWS_FILENAME)
for username in ["bobbarnes37", "alicebarnes79", "frankvanvleet40"]:
    new_row = {"follower" : "ellenbelbeck", "following" : username}
    df.loc[len(df)] = new_row

for username in ["frankwatanabe15", "bobsiakam68"]:
    new_row = {"follower" : "ellenbelbeck", "following" : username}
    df.loc[len(df)] = new_row
    new_row = {"follower" : username, "following": "ellenbelbeck"}
    df.loc[len(df)] = new_row
df.to_csv(FOLLOWS_FILENAME, index=False)

# make custom other stuff
df = pd.read_csv(FAVACTOR_FILENAME)
for actor in ["nm3154303", "nm4043618", "nm0702841"]:
    new_row = {"userID" : "ellenbelbeck", "actorID" : actor}
    df.loc[len(df)] = new_row
df.to_csv(FAVACTOR_FILENAME, index=False)

df = pd.read_csv(FAVGENRE_FILENAME)
for genre in ["g01", "g07", "g00"]:
    new_row = {"userID" : "ellenbelbeck", "genreID" : genre}
    df.loc[len(df)] = new_row
df.to_csv(FAVGENRE_FILENAME, index=False)

df=pd.read_csv(WATCHED_FILENAME)
for movieID in ["tt2382320", "tt1630029", "tt3480822"]:
    new_row = {"userID" : "ellenbelbeck", "movieID" : movieID, "lastWatched" : "2021-01-15", "likes" : 1}
    df.loc[len(df)] = new_row
df.to_csv(WATCHED_FILENAME, index=False)

