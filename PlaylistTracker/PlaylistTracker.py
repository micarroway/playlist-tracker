# -*- coding: utf-8 -*-
"""
Created on Thu Jun 22 09:01:41 2017

@author: JCatoe
"""
from PlaylistTracker.SpotifyClient import SpotifyClient
from PlaylistTracker.User import User
from PlaylistTracker.Users import Users

from PlaylistTracker.AppConfig import AppConfig


import numpy as np
import pandas as p
import matplotlib.pyplot as plt

class PlaylistTracker:
    __slots__ = ['users', 'sp']

    def __init__(self):
        self.users = Users(allowed_minutes=AppConfig.config['playlist']['allowed_minutes'])
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

        #Visualization MMills
        n_users = len(self.users)
        fig, chart = plt.subplots()
        index = np.arange(n_users)
        bar_width = 0.5
        opacity = .35

        user_names = []
        users_time = []#total time in min for each users' song additions
        time_allowed = []
        
        for user in self.users.values():
                user_names.append(user.username)
        
        for user in self.users.values():
                users_time.append(user.total_seconds/60000)       
                time_allowed.append((self.users.allowed_minutes/n_users) - (user.total_seconds/60000))
            
        bars1 = plt.bar(index, users_time,bar_width, alpha = opacity, color = 'g')

        bars2 = plt.bar(index, time_allowed, bar_width, alpha = opacity, color = 'k',
                                  bottom=users_time)
    
        plt.xlabel('Users')
        plt.ylabel('Time(minutes)')
        plt.title('Chicago Playlist: Total Time by User')        
        plt.tight_layout()
        plt.xticks(index,user_names)    
        #Visualization end    



    def add_tracks_to_users(self, tracks):
        for track in tracks:
            user_id = track['added_by']['id']
            if user_id not in self.users:
                self.users[user_id] = User(user_id)
            self.users.add_track(user_id, track['track'])

