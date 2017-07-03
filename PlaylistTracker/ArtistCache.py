from .SpotifyClient import SpotifyClient
import pickle
import os.path
from spotipy.client import SpotifyException


"""
A simple dictionary wrapped around automatic pickling
"""

class ArtistCache:
    __slots__ = ['autoload_from_disk', 'autosave_to_disk', '_cache', '_dumpFilePath']
    # static spotipy client unique to this class
    sp = SpotifyClient.get_client()

    def __init__(self, autoload_from_disk=True, autosave_to_disk=True):
        """

        :param autoload_from_disk: flag to load from pickle on __init__
        :param autosave_to_disk: flag to save to disk after adding a new artist
        """
        self.autoload_from_disk = autoload_from_disk
        self.autosave_to_disk = autosave_to_disk
        # The location of the pickle save file
        self._dumpFilePath = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'artistCache._cache')
        # load the pickle dump if it exists
        if self.autoload_from_disk and os.path.exists(self._dumpFilePath):
            try:
                self.load_from_disk()
            except TypeError as e:
                print(e.__class__)
        else:
            self._cache = {}

    def get_artist(self, artist_id):
        """

        :param artist_id: the spotify artist id to add
        :return: (artist dict from spotify api, boolean to indicate if we loaded from our cache)
        """
        loaded_from_cache = True

        # if artist is not in the cache, lookup via spotify api
        if artist_id not in self._cache:
            try:
                artist = self.sp.artist(artist_id)
            except SpotifyException:
                raise
            self.set_artist(artist)
            if self.autosave_to_disk:
                self.save_to_disk()
            # we loaded this artist from spotify, so set this to False
            loaded_from_cache = False

        return self._cache[artist_id], loaded_from_cache

    def set_artist(self, artist):
        """
        Adds a single artist dict to our cache
        :param artist: spotify dict returned from their api
        :return: None
        """
        if isinstance(artist, dict) and 'id' in artist:
            self._cache[artist['id']] = artist
        else:
            print("JUROBN")
            print(artist)

    def save_to_disk(self):
        """
        Saves cache to disk
        :return: None
        """
        with open(self._dumpFilePath, 'wb') as handle:
            pickle.dump(self._cache, handle, protocol=pickle.HIGHEST_PROTOCOL)

    def load_from_disk(self):
        """
        Loads cache from disk
        :return: None
        """
        with open(self._dumpFilePath, 'rb') as handle:
            self._cache = pickle.load(handle)
