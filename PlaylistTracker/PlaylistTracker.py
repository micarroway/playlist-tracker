# -*- coding: utf-8 -*-
"""
Created on Thu Jun 22 09:01:41 2017

@author: JCatoe
"""
from PlaylistTracker.SpotifyClient import SpotifyClient
from PlaylistTracker.User import User
from PlaylistTracker.Users import Users

from PlaylistTracker.AppConfig import AppConfig


class PlaylistTracker:
    __slots__ = ['users', 'sp']

    def __init__(self):
        self.users = Users()
        self.users.allowed_minutes = AppConfig.config['playlist']['allowed_minutes']
        # get a spotify client
        self.sp = SpotifyClient.get_client()

    def track_playlist(self):
        # get the playlist
        playlist = self.sp.user_playlist(AppConfig.config['playlist']['userID'],
                                         AppConfig.config['playlist']['playlistID'],
                                         fields='tracks,next')

        # extract first "chunk" of tracks and all subsequent "chunks"
        tracks = playlist['tracks']
        self.add_tracks_to_users(tracks['items'])
        while tracks['next']:
            tracks = self.sp.next(tracks)
            self.add_tracks_to_users(tracks['items'])

        # show results
        print(self.users)

    def add_tracks_to_users(self, tracks):
        for track in tracks:
            user_id = track['added_by']['id']
            if user_id not in self.users:
                self.users[user_id] = User(user_id)
            self.users.add_track(user_id, track['track'])
