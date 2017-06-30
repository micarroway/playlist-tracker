# -*- coding: utf-8 -*-
"""
Created on Thu Jun 22 09:01:41 2017

@author: JCatoe
"""

from User import User
from Users import Users
from SpotifyClient import SpotifyClient
from AppConfig import AppConfig

USERS = Users()
USERS.allowed_minutes = AppConfig.config['playlist']['allowed_minutes']


def add_tracks_to_users(tracks):
    for track in tracks:
        user_id = track['added_by']['id']
        if user_id not in USERS:
            USERS[user_id] = User(user_id)
        USERS.add_track(user_id, track['track'])


if __name__ == '__main__':

    # get a spotify client
    sp = SpotifyClient.get_client()

    # get the playlist
    playlist = sp.user_playlist(AppConfig.config['playlist']['userID'],
                                AppConfig.config['playlist']['playlistID'],
                                fields='tracks,next')

    # extract first "chunk" of tracks and all subsequent "chunks"
    tracks = playlist['tracks']
    add_tracks_to_users(tracks['items'])
    while tracks['next']:
        tracks = sp.next(tracks)
        add_tracks_to_users(tracks['items'])

    # show results
    print(USERS)
