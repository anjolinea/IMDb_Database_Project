import unittest
from app import app
import sqlite3
from toy_dataset.toy_dataset_consts import *
from toy_dataset.use_toy_dataset_util import load_csv_to_sql

def create_db_session():
    conn = sqlite3.connect(':memory:')
    # Read the schema SQL from your original schema and execute it on the test database
    with open('schema.sql', 'r') as f:
        schema_sql = f.read()
    conn.executescript(schema_sql)
    
    return conn

class TestDatabase(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.db = create_db_session()

    def tearDown(self):
        self.db.close()
        pass

    def test_db_populate(self):
        """Database population"""
        csv_files = [MOVIE_FILENAME, GENRE_FILENAME, MOVIEGENRE_FILENAME, ACTOR_FILENAME, STARRED_FILENAME, ROLE_FILENAME,
                 USER_FILENAME, FOLLOWS_FILENAME, FAVACTOR_FILENAME, FAVGENRE_FILENAME, WATCHED_FILENAME]
        insert_strings = ["Movie (movieID, movieTitle, movieRating, runtime, yearReleased, posterImgLink) VALUES (?, ?, ?, ?, ?, ?)",
                    "Genre (genreID, genreName) VALUES (?, ?)",
                    "MovieGenre (movieID, genreID) VALUES (?, ?)",
                    "Actor (actorID, actorName) VALUES (?, ?)",
                    "Starred (movieID, actorID) VALUES (?, ?)",
                    "ActorRole (movieID, actorID, roleName) VALUES (?, ?, ?)",
                    "User (username, firstName, lastName, userPassword, profilePicLink) VALUES (?, ?, ?, ?, ?)",
                    "Follows (userID1, userID2) VALUES (?, ?)",
                    "FavActor (userID, actorID) VALUES (?, ?)",
                    "FavGenre (userID, genreID) VALUES (?, ?)",
                    "Watched (userID, movieID, lastWatched, likes) VALUES (?, ?, ?, ?)"
                    ]
        for i in range(len(csv_files)):
            load_csv_to_sql(connection=self.db, csv_filename="toy_dataset/"+csv_files[i], insert_string=insert_strings[i])
        self.assertEqual(True, True)

if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(unittest.TestLoader().loadTestsFromTestCase(TestDatabase))
