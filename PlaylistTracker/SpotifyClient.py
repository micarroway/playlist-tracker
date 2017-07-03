import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

from .AppConfig import AppConfig


class SpotifyClient:
    __oath = AppConfig.config['oath']
    client = spotipy.Spotify(
        client_credentials_manager=SpotifyClientCredentials(
            client_id=__oath['client_id'],
            client_secret=__oath['client_secret']
        )
    )

    """
    static methods are methods we can call with creating a new SpotifyClient object
    this will return the same spotipy client every time you run SpotipyClient.get_client()
    """

    @staticmethod
    def get_client():
        """
        Returns a global instance of a spotipy client with our credentials
        :return spotipy.Spotify instance
        """
        return SpotifyClient.client
