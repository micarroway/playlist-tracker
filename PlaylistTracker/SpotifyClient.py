import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

from .AppConfig import AppConfig


class SpotifyClient:

    """
    static methods are methods we can call with creating a new SpotifyClient object
    this will create a new spotipy client every time you run SpotipyClient.get_client()
    """
    @staticmethod
    def get_client():
        """
        Returns a new instance of a spotipy client with our credentials
        :return spotipy.Spotify instance
        """
        oath = AppConfig.config['oath']
        return spotipy.Spotify(
            client_credentials_manager=SpotifyClientCredentials(
                client_id=oath['client_id'],
                client_secret=oath['client_secret']
            )
        )
