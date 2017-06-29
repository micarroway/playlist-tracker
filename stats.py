# -*- coding: utf-8 -*-
"""
Created on Thu Jun 22 09:01:41 2017

@author: JCatoe
"""
import json
from operator import itemgetter

import spotipy
import spotipy.util as util

from User import User


with open('spotify_config.json') as config:
    config = json.load(config)

token = util.prompt_for_user_token(**config['oath'])
sp = spotipy.Spotify(auth=token)

USERS = {}
UNIQUE_USER_IDS = set()
AVG_POP = []
SONGS = []


def ms_to_min(ms):
    return(round(ms/60000, 2))

# JUROBN get what data? I can't tell what this method does without looking at the code.
#   I would suggest populate_user_stats_from_tracks since you dont actual return data
def get_data(tracks):
    for i, item in enumerate(tracks['items']):
        # JUROBN I'm not familiar with python common practices with local variables names.
        # Do they want you to underscore them or is this just something you like?
        user_id = item['added_by']['id']
        if user_id not in UNIQUE_USER_IDS:
            UNIQUE_USER_IDS.add(user_id)
        SONGS.append(item['track'])
        # updates dictionary
        _pop = item['track']['popularity']
        if user_id not in USERS:
            USERS[user_id] = User(user_id)
        user = USERS[user_id]
        user.song_count += 1
        user.total_time += item['track']['duration_ms']
        user.popularity.append(_pop)
    return(total)

# JUROBN define "clean" data. better method names
def collect_clean_data():
    data = []
    for _id in UNIQUE_USER_IDS:
        user = USERS[_id]
        _person = user.display_name
        _song_count = str(user.song_count)
        _total_time = str(ms_to_min(user.total_time))
        # JUROBN good job not keeping a running average. However, you don't need to store all the individual popularity ratings.
        #   You just need to store the sum so far and the count so far. This will reduce time and space complexity from O(n) to O(1)
        #   it would also eliminate the need for your AVG_POP variable
        _avg = sum(user.popularity) / len(user.popularity)
        _pop = str(round(_avg, 2))
        # JUROBN why store the popularities in their own variable if you have the data already?
        for score in user.popularity:
            AVG_POP.append(score)
        data.append([_person, _song_count, _total_time, _pop])
    return(data)


def total_mins():
    _total_time = 0
    for _id in UNIQUE_USER_IDS:
        _total_time += USERS[_id].total_time
    return(ms_to_min(_total_time))


def average_popularity():
    _avg = sum(AVG_POP) / len(AVG_POP)
    pop = str(round(_avg, 2))
    return(str(pop))


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
                                                    str(total_mins()).rjust(3),
                                                    str(average_popularity()).rjust(5)))
    print()
    is_time_over(total_mins(), data)


if __name__ == '__main__':
    total = 0
    chicago = sp.user_playlist(config['playlist']['userID'], config['playlist']['playlistID'])
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
