from unittest import TestCase
from PlaylistTracker.Users import Users


class TestUsers(TestCase):
    def setUp(self):
        self.users = Users()

    def test___setitem__(self):
        with self.assertRaises(NotImplementedError):
            self.users[0] = 'not a User class'
