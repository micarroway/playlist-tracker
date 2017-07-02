import spotipy
from  spotipy.oauth2 import SpotifyClientCredentials
import spotipy.util as util

from .AppConfig import AppConfig


class SpotifyClient:
    @staticmethod
    def get_client():
        oath = AppConfig.config['oath']
        return spotipy.Spotify(
            client_credentials_manager=SpotifyClientCredentials(
                client_id=oath['client_id'],
                client_secret=oath['client_secret']
            )
        )
