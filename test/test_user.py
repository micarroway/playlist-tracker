import unittest

from PlaylistTracker.User import User


class TestUser(unittest.TestCase):
    def setUp(self):
        self.user = User('test')
        self.user.add_track({'popularity': 10, 'duration_ms': 50000, 'artists': [{'id': '2e898fil1F5umrc2LBtV93'}]})
        self.user.add_track({'popularity': 20, 'duration_ms': 40000, 'artists': [{'id': '2e898fil1F5umrc2LBtV93'}]})

    def test_get_total_minutes(self):
        self.assertEqual(self.user.get_total_minutes(), 1.5)

    def test_add_track(self):
        self.assertEqual(self.user.num_tracks, 2)
        self.user.add_track({'popularity': 15, 'duration_ms': 30000, 'artists': [{'id': '2e898fil1F5umrc2LBtV93'}]})
        self.assertEqual(self.user.num_tracks, 3)

    def test_get_average_popularity(self):
        self.assertEqual(self.user.get_average_popularity(), 15)
        self.user.add_track({'popularity': 30, 'duration_ms': 30000, 'artists': [{'id': '2e898fil1F5umrc2LBtV93'}]})
        self.assertEqual(self.user.get_average_popularity(), 20)
        self.user.add_track({'popularity': 5, 'duration_ms': 30000, 'artists': [{'id': '2e898fil1F5umrc2LBtV93'}]})
        self.assertEqual(self.user.get_average_popularity(), 16.25)


if __name__ == '__main__':
    unittest.main()
