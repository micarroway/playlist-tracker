from unittest import TestCase
from PlaylistTracker.ArtistCache import ArtistCache


class TestArtistCache(TestCase):
    artist_id = '2e898fil1F5umrc2LBtV93'

    def setUp(self):
        self.artistCache = ArtistCache(autoload_from_disk=False, autosave_to_disk=False)

    def test_get_artist(self):
        artist, loaded_from_cache = self.artistCache.get_artist(self.artist_id)
        self.assertFalse(loaded_from_cache)
        artist, loaded_from_cache = self.artistCache.get_artist(self.artist_id)
        self.assertTrue(loaded_from_cache)