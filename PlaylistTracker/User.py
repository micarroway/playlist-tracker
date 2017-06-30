from PlaylistTracker.SpotifyClient import SpotifyClient


class User:
    sp = SpotifyClient.get_client()

    __slots__ = ['username', 'popularity', 'song_count', 'total_seconds',
                 'artist', 'genres', '_spotify_profile', 'display_name']

    def __init__(self, username):
        self.username = username
        self.popularity = 0
        self.song_count = 0
        self.total_seconds = 0
        self.genres = []
        self._spotify_profile = self.sp.user(self.username)
        self.display_name = self._spotify_profile['display_name'] or self._spotify_profile['id']

    def __repr__(self):
        return repr((self.display_name, self.song_count, self.total_seconds, self.get_average_popularity()))

    def __str__(self):
        return '%s: %s songs, %s mins, %s Avg Popularity' % (self.display_name.rjust(20),
                                                             str(self.song_count).rjust(3),
                                                             str(round(self.get_total_minutes(), 2)).rjust(7),
                                                             str(round(self.get_average_popularity(), 2)).rjust(5))

    def get_total_minutes(self):
        return self.total_seconds / 60000

    def get_genres(self, artist):
        artist_genres = []
        results = self.sp.search(q='artist:' + artist, type='artist')
        for result in results['artists']['items']:
            if result['genres']:
                for genre in result['genres']:
                    if genre not in artist_genres:
                        artist_genres.append(genre)
        return(artist_genres)

    def add_track(self, track):
        self.popularity += track['popularity']
        self.song_count += 1
        self.total_seconds += track['duration_ms']
        self.artist = track['artists'][0]['name']
        self.genres.append(self.get_genres(self.artist))

    def get_average_popularity(self):
        if not self.song_count:
            return 0
        return self.popularity / self.song_count
