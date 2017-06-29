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


# JUROBN get what data? I can't tell what this method does without looking at the code.
#   I would suggest populate_user_stats_from_tracks since you dont actual return data
def get_data(tracks):
    for i, item in enumerate(tracks['items']):
        user_id = item['added_by']['id']
        if user_id not in USERS:
            USERS[user_id] = User(user_id)
        USERS.add_track(user_id, item['track'])


if __name__ == '__main__':
    total = 0
    sp = SpotifyClient.get_client()
    chicago = sp.user_playlist(AppConfig.config['playlist']['userID'], AppConfig.config['playlist']['playlistID'])
    owner = chicago['owner']['id']
    results = sp.user_playlist(owner,
                               chicago['id'],
                               fields='tracks,next')
    tracks = results['tracks']
    get_data(tracks)
    while tracks['next']:
        tracks = sp.next(tracks)
        get_data(tracks)

    print(USERS)
