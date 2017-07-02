from .SpotifyClient import SpotifyClient
import pickle
import os.path


class ArtistCache:
    __slots__ = ['autoload_from_disk', 'autosave_to_disk', '_cache', '_dumpFilePath']
    sp = SpotifyClient.get_client()

    def __init__(self, autoload_from_disk=True, autosave_to_disk=True):
        self.autoload_from_disk = autoload_from_disk
        self.autosave_to_disk = autosave_to_disk
        self._dumpFilePath = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'artistCache._cache')
        if self.autoload_from_disk and os.path.exists(self._dumpFilePath):
            try:
                self.load_from_disk()
            except TypeError as e:
                print(e.__class__)
        else:
            self._cache = {}

    def get_artist(self, artist_id):
        loaded_from_cache = True

        if artist_id not in self._cache:
            self.set_artist(self.sp.artist(artist_id))
            if self.autosave_to_disk:
                self.save_to_disk()
            loaded_from_cache = False

        return self._cache[artist_id], loaded_from_cache

    def set_artist(self, artist):
        self._cache[artist['id']] = artist

    def save_to_disk(self):
        with open(self._dumpFilePath, 'wb') as handle:
            pickle.dump(self._cache, handle, protocol=pickle.HIGHEST_PROTOCOL)

    def load_from_disk(self):
        with open(self._dumpFilePath, 'rb') as handle:
            self._cache = pickle.load(handle)
