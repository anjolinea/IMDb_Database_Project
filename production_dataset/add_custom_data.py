## For adding custom data to the toy dataset so we can test it

import pandas as pd
from prod_dataset_consts import *
from werkzeug.security import generate_password_hash

# add custom person whose username we know
df = pd.read_csv(USER_FILENAME)

if not ((df["username"] == "ellenbelbeck").any()):
    password = generate_password_hash("abcABC1234", method='scrypt')
    new_row = {'username': 'ellenbelbeck', 'firstName': 'Ellen', 'lastName': 'Belbeck', 'userPassword' : password, 'profilePicLink' : "https://hips.hearstapps.com/hmg-prod/images/gettyimages-1052566600.jpg"}
    df.loc[len(df)] = new_row
    df.to_csv(USER_FILENAME, index=False)

    # make custom person follow people
    df = pd.read_csv(FOLLOWS_FILENAME)
    for username in ["jessicarivera15", "samuelcollins85", "jeremyflores77"]:
        new_row = {"follower" : "ellenbelbeck", "following" : username}
        df.loc[len(df)] = new_row

    for username in ["victorcarter31", "johnnymorgan47"]:
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

df = pd.read_csv(USER_FILENAME)
df.loc[df.username == "jeremyflores77",'profilePicLink'] = "https://upload.wikimedia.org/wikipedia/commons/3/31/CA_FloresEurochamp_Leroy_028.jpg"
df.loc[df.username == "jessicarivera15",'profilePicLink'] = "https://i.guim.co.uk/img/media/ce99d9d35ebea0b35a7339fff30e4f92e60e0af4/1274_194_2993_1796/master/2993.jpg?width=1200&height=1200&quality=85&auto=format&fit=crop&s=2602da10b130e3d69c10dd4dff79bf2a"
df.loc[df.username == "johnnymorgan47",'profilePicLink'] = "https://upload.wikimedia.org/wikipedia/commons/e/eb/2004_-_ringo_thankspage_thumb.jpg"
df.loc[df.username == "victorcarter31", "profilePicLink"] = "https://espnpressroom.com/us/files/2020/09/Carter-Card-scaled-e1673627819233.jpg"
df.loc[df.username == "samuelcollins85", "profilePicLink"] = "https://pbs.twimg.com/profile_images/447799578205503488/UwtfbsGa_400x400.png"
df.loc[df.username == "ellenbelbeck", "profilePicLink"] = "https://hips.hearstapps.com/hmg-prod/images/gettyimages-1052566600.jpg"
df.to_csv(USER_FILENAME, index=False)