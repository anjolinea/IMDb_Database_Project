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

def populate_db(conn):
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
    csv_counter = 0
    for i in range(len(csv_files)):
        load_csv_to_sql(connection=conn, csv_filename="toy_dataset/"+csv_files[i], insert_string=insert_strings[i])
        csv_counter += 1
    
    return csv_counter


class TestDatabasePop(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.db = create_db_session()

    def tearDown(self):
        self.db.close()
        pass

    def test_db_populate(self):
        """database population"""
        
        self.assertEqual(populate_db(self.db), 11)
    
    def test_db_populate(self):
        """populated value count"""
        
        populate_db(self.db)
        cursor = self.db.cursor()

        cursor.execute("SELECT * FROM Movie")
        self.assertEqual(len(cursor.fetchall()), 20)

        cursor.execute("SELECT * FROM Genre")
        self.assertEqual(len(cursor.fetchall()), 8)

        cursor.execute("SELECT * FROM MovieGenre")
        self.assertEqual(len(cursor.fetchall()), 57)

        cursor.execute("SELECT * FROM Actor")
        self.assertEqual(len(cursor.fetchall()), 76)

        cursor.execute("SELECT * FROM Starred")
        self.assertEqual(len(cursor.fetchall()), 80)

        cursor.execute("SELECT * FROM ActorRole")
        self.assertEqual(len(cursor.fetchall()), 92)

        cursor.execute("SELECT * FROM User")
        self.assertEqual(len(cursor.fetchall()), 31)

        cursor.execute("SELECT * FROM Follows")
        self.assertEqual(len(cursor.fetchall()), 87)

        cursor.execute("SELECT * FROM FavActor")
        self.assertEqual(len(cursor.fetchall()), 63)

        cursor.execute("SELECT * FROM FavGenre")
        self.assertEqual(len(cursor.fetchall()), 53)

        cursor.execute("SELECT * FROM Watched")
        self.assertEqual(len(cursor.fetchall()), 115)


if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(unittest.TestLoader().loadTestsFromTestCase(TestDatabasePop))
