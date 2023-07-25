import unittest
from werkzeug.security import generate_password_hash, check_password_hash
from website.models import UserAuth

class TestUser(unittest.TestCase):

    def setUp(self):

        # user test values
        self.testUsername1 = 'testuser1'
        self.testUsername2 = 'testuser2'
        self.testUsername3 = 'testuser3'
        self.strongPassword = 'StrongPassw0rd'
        self.otherStrongPassword = 'otherStrongPassw0rd'
        self.anotherStrongPassword = 'anotherStrongPassw0rd'

    def tearDown(self):
        pass

    def test_password_hash(self):
        """password hash test"""
        strongPasswordHash = generate_password_hash(self.strongPassword, method='scrypt')
        otherStrongPasswordHash = generate_password_hash(self.otherStrongPassword, method='scrypt')
        anotherStrongPasswordHash = generate_password_hash(self.anotherStrongPassword, method='scrypt')

        self.assertEqual(check_password_hash(strongPasswordHash, self.strongPassword), True)
        self.assertEqual(check_password_hash(otherStrongPasswordHash, self.otherStrongPassword), True)
        self.assertEqual(check_password_hash(anotherStrongPasswordHash, self.anotherStrongPassword), True)

    def test_user_model(self):
        """user test"""
        passwordHash1 = generate_password_hash(self.strongPassword, method='scrypt')
        user1 = UserAuth(username=self.testUsername1, userPasswordHash=passwordHash1)

        passwordHash2 = generate_password_hash(self.strongPassword, method='scrypt')
        user2 = UserAuth(username=self.testUsername2, userPasswordHash=passwordHash2)

        passwordHash3 = generate_password_hash(self.strongPassword, method='scrypt')
        user3 = UserAuth(username=self.testUsername3, userPasswordHash=passwordHash3)

        self.assertEqual(user1.get()[0], self.testUsername1)
        self.assertEqual(user2.get()[0], self.testUsername2)
        self.assertEqual(user3.get()[0], self.testUsername3)
        self.assertEqual(user1.get()[1], passwordHash1)
        self.assertEqual(user2.get()[1], passwordHash2)
        self.assertEqual(user3.get()[1], passwordHash3)

if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(unittest.TestLoader().loadTestsFromTestCase(TestUser))