from .ArtistCache import ArtistCache
from .SpotifyClient import SpotifyClient
from spotipy.client import SpotifyException


class User:
    sp = SpotifyClient.get_client()
    artistCache = ArtistCache()

    __slots__ = ['username', 'popularity', 'num_tracks', 'total_seconds', 'genres', '_spotify_profile', 'display_name']

    def __init__(self, username):
        self.username = username
        self.popularity = 0
        self.num_tracks = 0
        self.total_seconds = 0
        self.genres = set()
        try:
            self._spotify_profile = self.sp.user(self.username)
            self.display_name = self._spotify_profile['display_name'] or self._spotify_profile['id']
        except SpotifyException:
            raise


    def __repr__(self):
        return repr((self.display_name, self.num_tracks, self.total_seconds, self.get_average_popularity()))

    def __str__(self):
        return '%s: %s songs, %s mins, %s Avg Popularity' % (self.display_name.rjust(20),
                                                             str(self.num_tracks).rjust(3),
                                                             str(round(self.get_total_minutes(), 2)).rjust(7),
                                                             str(round(self.get_average_popularity(), 2)).rjust(5))

    def get_total_minutes(self):
        return float(self.total_seconds) / 60000

    def add_genre_by_artist_id(self, artist_id):
        artist, loaded_from_cache = self.artistCache.get_artist(artist_id)
        self.add_genres(artist['genres'])

    def add_genres(self, genres):
        self.genres.update(genres)

    def add_genre(self, genre):
        self.genres.add(genre)

    def add_track(self, track):
        self.popularity += track['popularity']
        self.num_tracks += 1
        self.total_seconds += track['duration_ms']
        for artist in track['artists']:
            self.add_genre_by_artist_id(artist['id'])

    def get_average_popularity(self):
        if not self.num_tracks:
            return 0
        return float(self.popularity) / self.num_tracks
