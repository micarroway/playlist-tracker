from unittest import TestCase
from PlaylistTracker.PlaylistTracker import PlaylistTracker


class TestPlaylistTracker(TestCase):
    def setUp(self):
        self.playlist_tracker = PlaylistTracker("1277120721", "6sV2iBPZVHkfLCcGOeUaaF", 1440, False)
        self.users = self.playlist_tracker.track_playlist()

    def test_track_playlist(self):
        self.assertGreater(len(self.users), 0, "Users should contain at least one user")

    def test_global_track_counter(self):
        self.assertGreater(self.users.get_num_tracks(), 0, "Users should have a global track count")
        track_count = sum(user.num_tracks for user in self.users.values())
        self.assertEqual(self.users.get_num_tracks(), track_count, "Global track count should equal summed track count")

    def test_global_track_counter_through_individual_user(self):
        user = next(iter(self.users.values()))
        user.add_track({'popularity': 0, 'duration_ms': 0, 'artists': []})
        track_count = sum(user.num_tracks for user in self.users.values())
        self.assertEqual(self.users.get_num_tracks(), track_count, "Global track count should equal summed track count after adding a track to a user directly")
