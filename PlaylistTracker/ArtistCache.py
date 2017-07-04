import os.path
import pickle

from spotipy.client import SpotifyException

from .SpotifyClient import SpotifyClient

"""
A simple dictionary wrapped around automatic pickling
"""


class ArtistCache(dict):
    __slots__ = ['autoload_from_disk', 'autosave_to_disk', '_cache_directory', '_cache_file_name', '_cache_file_path']
    # static spotipy client unique to this class
    sp = SpotifyClient.get_client()
    CACHE_DIRECTORY_NAME = 'artist_cache'

    def __init__(self, autoload_from_disk=True, autosave_to_disk=True):
        """

        :param autoload_from_disk: flag to load from pickle on __init__
        :param autosave_to_disk: flag to save to disk after adding a new artist
        """
        self.autoload_from_disk = autoload_from_disk
        self.autosave_to_disk = autosave_to_disk
        # The location of the pickle save file
        self._cache_directory = os.path.join(os.path.dirname(os.path.realpath(__file__)), ArtistCache.CACHE_DIRECTORY_NAME)
        self._cache_file_name = str(pickle.HIGHEST_PROTOCOL) + ".dat"
        self._cache_file_path = os.path.join(self._cache_directory, self._cache_file_name)
        # load the pickle dump if it exists
        initial_data = {}
        if self.autoload_from_disk:
            try:
                initial_data = self.load_from_disk()
            except TypeError as e:
                print("Error loading artist cache from disk " + str(e))

        dict.__init__(self, initial_data)

    def get_artist(self, artist_id):
        """

        :param artist_id: the spotify artist id to add
        :return: (artist dict from spotify api, boolean to indicate if we loaded from our cache)
        """
        loaded_from_cache = True

        # if artist is not in the cache, lookup via spotify api
        if artist_id not in self:
            try:
                artist = self.sp.artist(artist_id)
            except SpotifyException:
                raise
            self.set_artist(artist)
            if self.autosave_to_disk:
                self.save_to_disk()
            # we loaded this artist from spotify, so set this to False
            loaded_from_cache = False

        return self[artist_id], loaded_from_cache

    def set_artist(self, artist):
        """
        Adds a single artist dict to our cache
        :param artist: spotify dict returned from their api
        :return: None
        """
        self[artist['id']] = artist

    def save_to_disk(self):
        """
        Saves cache to disk
        :return: None
        """
        if not os.path.exists(self._cache_directory):
            os.makedirs(self._cache_directory)
        with open(self._cache_file_path, 'wb') as handle:
            pickle.dump(self, handle, protocol=pickle.HIGHEST_PROTOCOL)

    def load_from_disk(self):
        """
        Loads cache from disk
        :return: None
        """
        if not os.path.exists(self._cache_file_path):
            return {}
        with open(self._cache_file_path, 'rb') as handle:
            return pickle.load(handle)
