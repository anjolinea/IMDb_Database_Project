# Because IMDb doesn't have a free API, we are using www.omdbapi.com to get 
# the links of the poster images. However, the API limits to 1000 searches per 
# day, so this part of the process is in a separate script. 

import json
import requests
import pandas as pd

from prod_dataset_consts import API_KEY, MOVIE_FILENAME

def get_movie_poster_link(api_key, movie_id):
    URL = f"https://www.omdbapi.com/?apikey={api_key}&i={movie_id}"
    page = requests.get(URL)

    if page.status_code == 404:
        poster_link = "too many calls"
        return poster_link

    json_obj = json.loads(page.text)

    if json_obj["Response"] == "True":
        try:
            poster_link = json_obj["Poster"]
        except:
            poster_link = "no poster link"
    else: 
        poster_link = "too many calls"

    return poster_link

movie_df = pd.read_csv(MOVIE_FILENAME)

if "posterImgLink" not in list(movie_df.columns):
    movie_df["posterImgLink"] = "not_filled_yet"

for index, row in movie_df.iterrows():
    if row["posterImgLink"] == "not_filled_yet":
        link = get_movie_poster_link(API_KEY, row["movieID"])
        if link == "too many calls":
            break
        elif link == "no poster link":
            movie_df.at[index,"posterImgLink"] = ""
        else:
            movie_df.at[index,"posterImgLink"] = link

movie_df.to_csv(MOVIE_FILENAME, index=False)
        




