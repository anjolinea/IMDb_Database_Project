import gzip
import pandas as pd
import json
from toy_dataset_consts import *

N = 20

# load in tsv data
with gzip.open(INPUT_BASICS_FILENAME, 'r') as gzfile: 
    movie_df = pd.read_csv(gzfile, sep='\t')
with gzip.open(INPUT_RATINGS_FILENAME, 'r') as gzfile: 
    ratings_df = pd.read_csv(gzfile, sep='\t')
with gzip.open(INPUT_PRINCIPALS_FILENAME, 'r') as gzfile: 
    principals_df = pd.read_csv(gzfile, sep='\t')
with gzip.open(INPUT_NAMES_FILENAME, 'r') as gzfile: 
    names_df = pd.read_csv(gzfile, sep='\t')

# initalize structures that will become tables
MovieGenre_df = pd.DataFrame({'movieID': pd.Series(dtype='str'),
                              'genreID' : pd.Series(dtype='str')})
genreIDtoName_map = dict()

# filter by condition
movie_df = movie_df.loc[(movie_df['titleType'] == "movie")]
movie_df = movie_df.loc[(movie_df['startYear'] != "\\N") & (movie_df['startYear'] >= "2020") & (movie_df['startYear'] <= "2022")]
movie_df = movie_df.loc[(movie_df['runtimeMinutes'] != "\\N") & (movie_df['genres'] != "\\N") & (movie_df["genres"].str.contains("Adult") == False)]

# merge on ratings
movie_df = movie_df.merge(ratings_df, on='tconst')

# take most recent movies
movie_df.sort_values('numVotes',ascending = False, inplace=True)
movie_df = movie_df.iloc[0:N]

# movie_df: drop unneeded columns
movie_df.drop(columns=['titleType', 'primaryTitle', "endYear", "isAdult", "numVotes"], inplace=True)

# choose actors/actresses from these movies
principals_df = principals_df[(principals_df['category'] == "actor") | (principals_df['category'] == "actress")]
principals_df = principals_df[(principals_df['ordering'] <= 9)]
starred_df = pd.merge(movie_df, principals_df, on='tconst', how="left")

# starred_df : drop unneeded columns
starred_df.drop(columns=["genres", "job", "category", "originalTitle", "startYear", "runtimeMinutes", "averageRating", "ordering"], inplace=True)

# starred_df : deal with characters
starred_df = starred_df.reset_index()  # make sure indexes pair with number of rows

roles_df = pd.DataFrame({'movieID': pd.Series(dtype='str'),
                        'actorID' : pd.Series(dtype='str'),
                        'role' : pd.Series(dtype="str")})
for index, row in starred_df.iterrows():
    loroles = json.loads(row["characters"])
    movieID = row["tconst"]
    actorID = row["nconst"]

    for role in loroles:
        # Define the new row to be added
        new_row = {'movieID': movieID, 'actorID': actorID, 'role': role}
        # Use the loc method to add the new row to the DataFrame
        roles_df.loc[len(roles_df)] = new_row

starred_df.drop(columns=["characters", "index"], inplace=True)

# deal with genre
for i in range(N):
    movie_genres = movie_df["genres"].iloc[i].split(",")
    for genre in movie_genres:
        if genre not in genreIDtoName_map:
            genreIDtoName_map[genre] = len(genreIDtoName_map)
        MovieGenre_df.loc[len(MovieGenre_df.index)] = [movie_df["tconst"].iloc[i], "g{:02d}".format(genreIDtoName_map[genre])]
movie_df.drop(columns=["genres"], inplace=True)

# create actors database from starred_df
actors_df = pd.merge(starred_df, names_df, on='nconst', how='left')

# actors_df : drop unneeded columns
actors_df.drop(columns=["tconst", "birthYear", "deathYear", "primaryProfession", "knownForTitles"], inplace=True)

# rename columns
movie_df.rename(columns={'tconst': 'movieID', 'originalTitle': 'movieTitle', 'startYear' : 'yearReleased', 'averageRating' : 'movieRating', 'runtimeMinutes' : 'runtime'}, inplace=True)
starred_df.rename(columns={'tconst': 'movieID', 'nconst' : 'actorID'}, inplace=True)
actors_df.rename(columns={'nconst' : 'actorID', 'primaryName' : 'actorName'}, inplace=True)

# genres
genres_df = pd.DataFrame([(i[1], i[0]) for i in genreIDtoName_map.items()], columns=['genreID', 'genreName'])
genres_df["genreID"] = genres_df["genreID"].apply(lambda x: "g{:02d}".format(x))

# actor duplicates
actors_df.drop_duplicates(inplace=True)

# movies reordering of columns
movie_df = movie_df[["movieID", "movieTitle", "movieRating", "runtime", "yearReleased"]]

# upload tables to CSV files
movie_df.to_csv(MOVIE_FILENAME, index=False)
MovieGenre_df.to_csv(MOVIEGENRE_FILENAME, index=False)
genres_df.to_csv(GENRE_FILENAME, index=False)
starred_df.to_csv(STARRED_FILENAME, index=False)
actors_df.to_csv(ACTOR_FILENAME, index=False)
roles_df.to_csv(ROLE_FILENAME, index=False)