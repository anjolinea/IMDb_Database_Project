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


class TestDatabaseProfile(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.db = create_db_session()

        # status codes
        self.REDIRECT_CODE = 302
        self.OK_CODE = 200

        # redirection
        self.SUCCESS_REDIR = '/login?next=%2Fprofile'
        self.FAILURE_REDIR = None

        # profile test values
        self.correctUser = 'ellenbelbeck'
        self.incorrectUser = 'iAmNotAUser'
        self.correctFirstname = 'Bob'
        self.incorrectFirstname = 'NotAFirstName'
        self.correctLastname = 'Watanabe'
        self.incorrectLastname = 'NotALastName'

    def tearDown(self):
        self.db.close()
        pass

    def test_db_profile_no_activity(self):
        """database profile no activity"""
        
        populate_db(self.db)
        response = self.app.post('/profile', data={"Follow": None, "Unfollow": None, "first": None, "last": None})
        self.assertEqual(response.status_code, self.REDIRECT_CODE)
        self.assertEqual(response.location, self.SUCCESS_REDIR)
    
    def test_db_profile_follow_success(self):
        """database profile follow success"""
        
        populate_db(self.db)
        response = self.app.post('/profile', data={"Follow": self.correctUser, "Unfollow": None, "first": None, "last": None})
        self.assertEqual(response.status_code, self.REDIRECT_CODE)
        self.assertEqual(response.location, self.SUCCESS_REDIR)
    
    def test_db_profile_follow_failure(self):
        """database profile follow failure"""
        
        populate_db(self.db)
        response = self.app.post('/profile', data={"Follow": self.incorrectUser, "Unfollow": None, "first": None, "last": None})
        self.assertEqual(response.status_code, self.REDIRECT_CODE)
        self.assertEqual(response.location, self.SUCCESS_REDIR)
    
    def test_db_profile_unfollow_success(self):
        """database profile unfollow success"""
        
        populate_db(self.db)
        response = self.app.post('/profile', data={"Follow": None, "Unfollow": self.correctUser, "first": None, "last": None})
        self.assertEqual(response.status_code, self.REDIRECT_CODE)
        self.assertEqual(response.location, self.SUCCESS_REDIR)
    
    def test_db_profile_unfollow_failure(self):
        """database profile unfollow failure"""
        
        populate_db(self.db)
        response = self.app.post('/profile', data={"Follow": None, "Unfollow": self.incorrectUser, "first": None, "last": None})
        self.assertEqual(response.status_code, self.REDIRECT_CODE)
        self.assertEqual(response.location, self.SUCCESS_REDIR)
    
    def test_db_profile_search_first_success(self):
        """database profile search first success"""
        
        populate_db(self.db)
        response = self.app.post('/profile', data={"Follow": None, "Unfollow": None, "first": self.correctFirstname, "last": None})
        self.assertEqual(response.status_code, self.REDIRECT_CODE)
        self.assertEqual(response.location, self.SUCCESS_REDIR)
    
    def test_db_profile_search_first_failure(self):
        """database profile search first failure"""
        
        populate_db(self.db)
        response = self.app.post('/profile', data={"Follow": None, "Unfollow": None, "first": self.incorrectFirstname, "last": None})
        self.assertEqual(response.status_code, self.REDIRECT_CODE)
        self.assertEqual(response.location, self.SUCCESS_REDIR)
    
    def test_db_profile_search_last_success(self):
        """database profile search last success"""
        
        populate_db(self.db)
        response = self.app.post('/profile', data={"Follow": None, "Unfollow": None, "first": None, "last": self.correctLastname})
        self.assertEqual(response.status_code, self.REDIRECT_CODE)
        self.assertEqual(response.location, self.SUCCESS_REDIR)
    
    def test_db_profile_search_last_failure(self):
        """database profile search last failure"""
        
        populate_db(self.db)
        response = self.app.post('/profile', data={"Follow": None, "Unfollow": None, "first": None, "last": self.incorrectLastname})
        self.assertEqual(response.status_code, self.REDIRECT_CODE)
        self.assertEqual(response.location, self.SUCCESS_REDIR)
    
    def test_db_profile_concurrent_success(self):
        """database profile concurrent success"""
        
        populate_db(self.db)
        response = self.app.post('/profile', data={"Follow": self.correctUser, "Unfollow": self.correctUser, "first": self.correctFirstname, "last": self.correctLastname})
        self.assertEqual(response.status_code, self.REDIRECT_CODE)
        self.assertEqual(response.location, self.SUCCESS_REDIR)
    
    def test_db_profile_concurrent_failure(self):
        """database profile concurrent failure"""
        
        populate_db(self.db)
        response = self.app.post('/profile', data={"Follow": self.incorrectUser, "Unfollow": self.incorrectUser, "first": self.incorrectFirstname, "last": self.incorrectLastname})
        self.assertEqual(response.status_code, self.REDIRECT_CODE)
        self.assertEqual(response.location, self.SUCCESS_REDIR)
    


if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(unittest.TestLoader().loadTestsFromTestCase(TestDatabaseProfile))
