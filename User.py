import json
import spotipy
import spotipy.util as util

with open('spotify_config.json') as config:
    config = json.load(config)


class User:

    token = util.prompt_for_user_token(**config['oath'])
    sp = spotipy.Spotify(auth=token)

    def __init__(self, username):
        self.username = username
        self.popularity = 0
        self.song_count = 0
        self.total_time = 0
        self._spotify_profile = self.sp.user(self.username)
        self.display_name = self._spotify_profile['display_name'] or self._spotify_profile['id']

    def get_total_minutes(self):
        return round(self.total_time/60000, 2)

    def add_track(self, track):
        self.popularity += track['popularity']
        self.song_count += 1
        self.total_time += track['duration_ms']

    def get_average_popularity(self):
        return self.popularity / self.song_count
