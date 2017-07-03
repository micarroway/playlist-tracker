# -*- coding: utf-8 -*-
"""
Created on Thu Jun 22 09:01:41 2017

@author: JCatoe
"""
from .SpotifyClient import SpotifyClient
from .User import User
from .Users import Users

import numpy as np
import matplotlib.pyplot as plt
from spotipy.client import SpotifyException


class PlaylistTracker:
    __slots__ = ['users', 'sp', 'user_id', 'playlist_id', 'allowed_minutes', 'show_gui_results']

    def __init__(self, user_id, playlist_id, allowed_minutes, show_gui_results=True):
        """

        :param user_id: the user id that owns the playlist
        :param playlist_id: the playlist id
        :param allowed_minutes: the total number of minutes allowed on the playlist
        :param show_gui_results: flag to show the gui version of minutes per user
        """
        self.user_id = user_id
        self.playlist_id = playlist_id
        self.allowed_minutes = allowed_minutes
        self.show_gui_results = show_gui_results
        self.users = Users(allowed_minutes=allowed_minutes)
        # get a spotify client
        self.sp = SpotifyClient.get_client()

    def track_playlist(self):
        """
        Computes and presents multiple statistics about our playlist

        :return: Users
        """

        # get the playlist
        try:
            playlist = self.sp.user_playlist(self.user_id, self.playlist_id, fields='tracks,next')
        except SpotifyException:
            raise

        # extract first "chunk" of tracks and all subsequent "chunks"
        tracks = playlist['tracks']
        self.add_tracks_to_users(tracks['items'])
        while tracks['next']:
            try:
                tracks = self.sp.next(tracks)
                self.add_tracks_to_users(tracks['items'])
            except SpotifyException:
                raise

        if self.show_gui_results:
            # Visualization MMills
            n_users = len(self.users)
            fig, chart = plt.subplots()
            index = np.arange(n_users)
            bar_width = 0.5
            opacity = .35

            user_names = [user.display_name for user in self.users.values()]
            users_time = [user.total_seconds / 60000 for user in self.users.values()]
            time_allowed = [(self.users.allowed_minutes / n_users) - (user.total_seconds / 60000)
                            for user in self.users.values()]

            bars1 = plt.bar(index, users_time, bar_width, alpha=opacity, color='g')

            bars2 = plt.bar(index, time_allowed, bar_width, alpha=opacity, color='k',
                            bottom=users_time)

            # some hardcoded colors for the masses
            bars1[0].set_color('#0276FD')
            bars1[2].set_color('#ff69b4')
            bars1[3].set_color('#4B0082')
            bars1[4].set_color('#7CFC00')
            bars1[5].set_color('#2F4F2F')
            bars1[6].set_color('#05B8CC')
            # end colors

            plt.xlabel('Users')
            plt.ylabel('Time(minutes)')
            plt.title('Chicago Playlist: Total Time by User')
            plt.tight_layout()
            plt.xticks(index, user_names, rotation="vertical")

            plt.show()
            # Visualization end

        return self.users

    def add_tracks_to_users(self, tracks):
        """
        Adds each track to our Users object
        :param tracks: list of tracks from Spotify api
        :return: None
        """
        for track in tracks:
            user_id = track['added_by']['id']
            if user_id not in self.users:
                self.users[user_id] = User(user_id)
            self.users.add_track(user_id, track['track'])
