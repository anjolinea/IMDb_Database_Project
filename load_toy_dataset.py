import gzip
import pandas as pd

INPUT_BASICS_FILENAME = "data/title.basics.tsv.gz"
INPUT_RATINGS_FILENAME = "data/title.ratings.tsv.gz"
INPUT_PRINCIPALS_FILENAME = "data/title.principals.tsv.gz"
INPUT_NAMES_FILENAME = "data/name.basics.tsv.gz"
MOVIES_FILENAME = "data/movies.csv"
MOVIEGENRE_FILENAME = "data/movieGenre.csv"
GENRES_FILENAME = "data/genres.csv"
STARRED_FILENAME = "data/starred.csv"
ACTOR_FILENAME = "data/actor.csv"

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
MovieGenre_df = pd.DataFrame({'movieID': pd.Series(dtype='int'),
                              'genreID' : pd.Series(dtype='int')})
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
movie_df.drop(columns=['titleType', 'primaryTitle', "endYear", "isAdult"], inplace=True)

# choose actors/actresses from these movies
principals_df = principals_df[(principals_df['category'] == "actor") | (principals_df['category'] == "actress")]
principals_df = principals_df[(principals_df['ordering'] <= 9)]
starred_df = pd.merge(movie_df, principals_df, on='tconst', how="left")

# starred_df : drop unneeded columns
starred_df.drop(columns=["genres", "job", "category", "originalTitle", "startYear", "runtimeMinutes", "averageRating","numVotes"], inplace=True)

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
actors_df.drop(columns=["tconst", "characters", "ordering"], inplace=True)

# rename columns
movie_df.rename(columns={'tconst': 'movieID', 'originalTitle': 'movieTitle', 'startYear' : 'yearReleased'}, inplace=True)
starred_df.rename(columns={'tconst': 'movieID', 'nconst' : 'actorID'}, inplace=True)
actors_df.rename(columns={'nconst' : 'actorID'}, inplace=True)

# genres
genres_df = pd.DataFrame(genreIDtoName_map.items(), columns=['genreName', 'genreID'])
genres_df["genreID"] = genres_df["genreID"].apply(lambda x: "g{:02d}".format(x))

# upload tables to CSV files
movie_df.to_csv(MOVIES_FILENAME, index=False)
MovieGenre_df.to_csv(MOVIEGENRE_FILENAME, index=False)
genres_df.to_csv(GENRES_FILENAME, index=False)
starred_df.to_csv(STARRED_FILENAME, index=False)
actors_df.to_csv(ACTOR_FILENAME, index=False)