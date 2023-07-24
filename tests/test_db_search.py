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


class TestDatabaseSearch(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.db = create_db_session()

        # status codes
        self.REDIRECT_CODE = 302
        self.OK_CODE = 200

        # redirection
        self.SUCCESS_REDIR = '/login?next=%2Fsearch'
        self.FAILURE_REDIR = None

        # search values
        self.correctTitle = 'spider-man'
        self.incorrectTitle = 'notAMovie'
        self.correctActor = 'tom holland'
        self.incorrectActor = 'notAnActor'
        self.correctGenre = 'Action'
        self.incorrectGenre = 'notAGenre'
        self.correctSort = 'rating_asc'
        self.incorrectSort = 'notASort'

    def tearDown(self):
        self.db.close()
        pass

    def test_db_search_title_success(self):
        """database search title success"""
        
        populate_db(self.db)
        response = self.app.post('/search', data={"title": self.correctTitle})
        self.assertEqual(response.status_code, self.REDIRECT_CODE)
        self.assertEqual(response.location, self.SUCCESS_REDIR)
    
    def test_db_search_title_failure(self):
        """database search title failure"""
        
        populate_db(self.db)
        response = self.app.post('/search', data={"title": self.incorrectTitle})
        self.assertEqual(response.status_code, self.REDIRECT_CODE)
        self.assertEqual(response.location, self.SUCCESS_REDIR)
    
    def test_db_search_actor_success(self):
        """database search actor success"""
        
        populate_db(self.db)
        response = self.app.post('/search', data={"actor": self.correctActor})
        self.assertEqual(response.status_code, self.REDIRECT_CODE)
        self.assertEqual(response.location, self.SUCCESS_REDIR)
    
    def test_db_search_actor_failure(self):
        """database search actor failure"""
        
        populate_db(self.db)
        response = self.app.post('/search', data={"actor": self.incorrectActor})
        self.assertEqual(response.status_code, self.REDIRECT_CODE)
        self.assertEqual(response.location, self.SUCCESS_REDIR)
    
    def test_db_search_genre_success(self):
        """database search genre success"""
        
        populate_db(self.db)
        response = self.app.post('/search', data={"genre": self.correctGenre})
        self.assertEqual(response.status_code, self.REDIRECT_CODE)
        self.assertEqual(response.location, self.SUCCESS_REDIR)
    
    def test_db_search_genre_failure(self):
        """database search genre failure"""
        
        populate_db(self.db)
        response = self.app.post('/search', data={"genre": self.incorrectGenre})
        self.assertEqual(response.status_code, self.REDIRECT_CODE)
        self.assertEqual(response.location, self.SUCCESS_REDIR)
    
    def test_db_search_sort_by_success(self):
        """database search sort-by success"""
        
        populate_db(self.db)
        response = self.app.post('/search', data={"sort-by": self.correctSort})
        self.assertEqual(response.status_code, self.REDIRECT_CODE)
        self.assertEqual(response.location, self.SUCCESS_REDIR)
    
    def test_db_search_sort_by_failure(self):
        """database search sort-by failure"""
        
        populate_db(self.db)
        response = self.app.post('/search', data={"sort-by": self.incorrectSort})
        self.assertEqual(response.status_code, self.REDIRECT_CODE)
        self.assertEqual(response.location, self.SUCCESS_REDIR)
    


if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(unittest.TestLoader().loadTestsFromTestCase(TestDatabaseSearch))
