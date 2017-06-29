import spotipy
import spotipy.util as util
from AppConfig import AppConfig


class SpotifyClient:
    @staticmethod
    def get_client():
        return spotipy.Spotify(auth=util.prompt_for_user_token(**AppConfig.config['oath']))
