import unittest
from app import app

class TestAuthentication(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()

        # status codes
        self.REDIRECT_CODE = 302
        self.OK_CODE = 200

        # redirection
        self.SUCCESS_REDIR = '/'
        self.FAILURE_REDIR = None

        # login test values
        self.correctUser = 'ellenbelbeck'
        self.incorrectUser = 'iAmNotAUser'
        self.correctPassword = 'abcABC1234'
        self.incorrectPassword = 'wrongpassword'

        # sign up test values
        self.testFirstName = 'Test'
        self.testLastName = 'User'
        self.testUsername = 'testuser'
        self.strongPassword = 'StrongPassw0rd'
        self.weakPassword = 'weakpassword'
        self.mismatchPassword1 = 'passwordmismatch'
        self.mismatchPassword2 = 'mismatchpassword'

    def tearDown(self):
        pass

    def test_login_success(self):
        """login success"""
        response = self.app.post('/login', data={'username': self.correctUser, 'password': self.correctPassword})
        self.assertEqual(response.status_code, self.REDIRECT_CODE)
        self.assertEqual(response.location, self.SUCCESS_REDIR)

    def test_login_failure_incorrect_password(self):
        """login failure: incorrect password"""
        response = self.app.post('/login', data={'username': self.correctUser, 'password': self.incorrectPassword})
        self.assertEqual(response.status_code, self.OK_CODE)
        self.assertEqual(response.location, self.FAILURE_REDIR)
    
    def test_login_failure_incorrect_user(self):
        """login failure: incorrect user"""
        response = self.app.post('/login', data={'username': self.incorrectUser, 'password': self.incorrectPassword})
        self.assertEqual(response.status_code, self.OK_CODE)
        self.assertEqual(response.location, self.FAILURE_REDIR)
    
    def test_signup_success(self):
        """sign up success"""
        response = self.app.post('/sign-up', data={"firstName": self.testFirstName, "lastName": self.testLastName, "username": self.testUsername, "password1": self.strongPassword, "password2": self.strongPassword})
        self.assertEqual(response.status_code, self.REDIRECT_CODE)
        self.assertEqual(response.location, self.SUCCESS_REDIR)
    
    def test_signup_failure_weak_password(self):
        """sign up failure: weak password"""
        response = self.app.post('/sign-up', data={"firstName": self.testFirstName, "lastName": self.testLastName, "username": self.testUsername, "password1": self.weakPassword, "password2": self.weakPassword})
        self.assertEqual(response.status_code, self.OK_CODE)
        self.assertEqual(response.location, self.FAILURE_REDIR)
    
    def test_signup_failure_password_mismatch(self):
        """sign up failure: password mismatch"""
        response = self.app.post('/sign-up', data={"firstName": self.testFirstName, "lastName": self.testLastName, "username": self.testUsername, "password1": self.mismatchPassword1, "password2": self.mismatchPassword2})
        self.assertEqual(response.status_code, self.OK_CODE)
        self.assertEqual(response.location, self.FAILURE_REDIR)
    
    def test_signup_failure_taken_username(self):
        """sign up failure: duplicate username"""
        response = self.app.post('/sign-up', data={"firstName": self.testFirstName, "lastName": self.testLastName, "username": self.testUsername, "password1": self.mismatchPassword1, "password2": self.mismatchPassword2})
        self.assertEqual(response.status_code, self.OK_CODE)
        self.assertEqual(response.location, self.FAILURE_REDIR)

if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(unittest.TestLoader().loadTestsFromTestCase(TestAuthentication))
