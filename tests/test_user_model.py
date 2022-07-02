import unittest
from app.models import User


class UserModelTestCase(unittest.TestCase):
    def setUp(self):
        self.u = User(password='cat')
        self.u2 = User(password='cat')


    def test_password_setter(self):
        self.assertTrue(self.u.password_hash is not None)

    
    def test_no_password_getter(self):
        with self.assertRaises(AttributeError):
            self.u.password


    def test_password_verification(self):
        self.assertTrue(self.u.verify_password('cat'))
        self.assertFalse(self.u.verify_password('dog'))


    def test_password_salts_are_random(self):
        self.assertTrue(self.u.password_hash != self.u2.password_hash)

        