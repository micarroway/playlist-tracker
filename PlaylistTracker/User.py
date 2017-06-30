import json
import spotipy
import spotipy.util as util

with open('spotify_config.json') as config:
    config = json.load(config)


class User:
    token = util.prompt_for_user_token(**config['oath'])
    sp = spotipy.Spotify(auth=token)

    __slots__ = ['username', 'popularity', 'song_count', 'total_seconds', '_spotify_profile', 'display_name']

    def __init__(self, username):
        self.username = username
        self.popularity = 0
        self.song_count = 0
        self.total_seconds = 0
        self._spotify_profile = self.sp.user(self.username)
        self.display_name = self._spotify_profile['display_name'] or self._spotify_profile['id']

    def __repr__(self):
        return repr((self.display_name, self.song_count, self.total_seconds, self.get_average_popularity()))

    def __str__(self):
        return '%s: %s songs, %s mins, %s Avg Popularity' % (self.display_name,
                                                             self.song_count,
                                                             round(self.get_total_minutes(), 2),
                                                             round(self.get_average_popularity(), 2))

    def get_total_minutes(self):
        return self.total_seconds / 60000

    def add_track(self, track):
        self.popularity += track['popularity']
        self.song_count += 1
        self.total_seconds += track['duration_ms']

    def get_average_popularity(self):
        return self.popularity / self.song_count
