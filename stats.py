# -*- coding: utf-8 -*-
"""
Created on Thu Jun 22 09:01:41 2017

@author: JCatoe
"""

from operator import itemgetter
from User import User
from Users import Users
from SpotifyClient import SpotifyClient
from AppConfig import AppConfig

USERS = Users()
SONGS = []

# JUROBN get what data? I can't tell what this method does without looking at the code.
#   I would suggest populate_user_stats_from_tracks since you dont actual return data
def get_data(tracks):
    for i, item in enumerate(tracks['items']):
        user_id = item['added_by']['id']
        SONGS.append(item['track'])
        if user_id not in USERS:
            USERS[user_id] = User(user_id)
        user = USERS[user_id]
        user.add_track(item['track'])

# JUROBN define "clean" data. better method names
def collect_clean_data():
    data = []
    for user in USERS.values():
        data.append([
            user.display_name,
            str(user.song_count),
            str(user.get_total_minutes()),
            str(user.get_average_popularity())])
    return data


def is_time_over(total_time, data):
    # JUROBN where does this number come from? I know it's calculated from car travel but how would someone else know? Maybe put in config.
    _allowed_minutes = 1440
    _limit = round(_allowed_minutes - total_time)
    _per_person_limit = _allowed_minutes / 7

    if total_time > _allowed_minutes:
        print('The total time is over the limit by %s mins.' % (_limit*-1))
    elif total_time == _allowed_minutes:
        print('Good job, guys.')
    else:
        print('The total time is under the limit by %s mins.' % _limit)

    for person in data:
        # JUROBN the fuck? person[2]?
        _personal_time = float(person[2])
        if _personal_time > _per_person_limit:
            _overage = str(round(_personal_time - _per_person_limit))
            print('      %s is over the limit by %s mins.' % (person[0].rjust(8),
                                                              _overage))
        if _personal_time < _per_person_limit:
            _under = str(round(_personal_time - _per_person_limit)*-1)
            print('      %s is under the limit by %s mins.' % (person[0].rjust(8),
                                                               _under))


def pprint(data):
    print()
    for person in data:
        # JUROBN what do these indices mean? You should make a class that holds the properties you are trying to show
            print('%s: %s songs, %s mins, %s Avg Popularity' % (person[0].rjust(8),
                                                                person[1].rjust(3),
                                                                person[2].rjust(6),
                                                                person[3]))
    print('--------------------------------------------------------')
    print('%s songs, %s mins, %s Avg Popularity' % (str(len(SONGS)).rjust(13),
                                                    str(USERS.get_total_minutes()).rjust(3),
                                                    str(USERS.get_average_popularity()).rjust(5)))
    print()
    is_time_over(USERS.get_total_minutes(), data)


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

    # JUROBN do you know the time complexity of the average sorting algorithm? It's a decent amount of overhead.
    sort_by = {'person': 0,
               'songs': 1,
               'time': 2,
               'popularity': 3}

    data = sorted(collect_clean_data(),
                  key=itemgetter(sort_by['songs']),
                  reverse=True)

    pprint(data)
