# -*- coding: utf-8 -*-
"""
Created on Thu Jun 22 09:01:41 2017

@author: JCatoe
"""
import json
from operator import itemgetter

import spotipy
import spotipy.util as util


with open('spotify_config.json') as config:
    config = json.load(config)

token = util.prompt_for_user_token(**config['oath'])
sp = spotipy.Spotify(auth=token)

# JUROBN You need a User class to represent each person. I would also suggest a Users class to hold them all.
# JUROBN Good use of dict for quick lookup. Do you know how dict/hashmaps work under the hood?
# JUROBN The names are fine in this small scope but in real code you don't to hard code names like this. I would see if could programatically pull them in, if not just show the username
# could take the trouble to create and update this in real time...
USERS = {'1277120721': {'person': 'Jaki',
                        'popularity': [],
                        'song_count': 0,
                        'total_time': 0},
         'cptyaimie': {'person': 'Jaimie',
                       'popularity': [],
                       'song_count': 0,
                       'total_time': 0},
         'taraterrrific': {'person': 'Tara',
                           'popularity': [],
                           'song_count': 0,
                           'total_time': 0},
         '1272969703': {'person': 'Nowah',
                        'popularity': [],
                        'song_count': 0,
                        'total_time': 0},
         '1236554442': {'person': 'Maritza',
                        'popularity': [],
                        'song_count': 0,
                        'total_time': 0},
         'phillipu': {'person': 'Phillip',
                      'popularity': [],
                      'song_count': 0,
                      'total_time': 0},
         'platypusmaximus': {'person': 'Justin',
                             'popularity': [],
                             'song_count': 0,
                             'total_time': 0}
         }

USERS_LIST = list(USERS.keys())
UNIQUE_IDS = []
AVG_POP = []
SONGS = []


def ms_to_min(ms):
    # JUROBN why not just one math operation? It's a small inefficiency but where do you draw the line?
    x = ms / 1000
    minutes = x / 60
    return(round(minutes, 2))


def is_new_id(test):
    # JUROBN you can just `return test not in UNIQUE_IDS`
    # JUROBN Is UNIQUE_IDS a dictionary or list? If it's a list this is O(n) time complexity, dictionary would reduce to O(1)
    # JUROBN UNIQUE_IDS is an ambiguous variable name even in this narrow spotify scope.
    #   ID of what? Track? User? Playlist? Something you created?
    if test in UNIQUE_IDS:
        return(False)
    else:
        return(True)


# JUROBN get what data? I can't tell what this method does without looking at the code.
#   I would suggest populate_user_stats_from_tracks since you dont actual return data
def get_data(tracks):
    for i, item in enumerate(tracks['items']):
        # JUROBN I'm not familiar with python common practices with local variables names.
        # Do they want you to underscore them or is this just something you like?
        _added_by = item['added_by']['id']
        if is_new_id(_added_by):
            UNIQUE_IDS.append(_added_by)
        SONGS.append(item['track'])
        # updates dictionary
        _pop = item['track']['popularity']
        USERS[_added_by]['song_count'] += 1
        USERS[_added_by]['total_time'] += item['track']['duration_ms']
        USERS[_added_by]['popularity'].append(_pop)
    return(total)

# JUROBN define "clean" data. better method names
def collect_clean_data():
    data = []
    for _id in UNIQUE_IDS:
        _person = USERS[_id]['person']
        _song_count = str(USERS[_id]['song_count'])
        _total_time = str(ms_to_min(USERS[_id]['total_time']))
        # JUROBN good job not keeping a running average. However, you don't need to store all the individual popularity ratings.
        #   You just need to store the sum so far and the count so far. This will reduce time and space complexity from O(n) to O(1)
        #   it would also eliminate the need for your AVG_POP variable
        _avg = sum(USERS[_id]['popularity']) / len(USERS[_id]['popularity'])
        _pop = str(round(_avg, 2))
        # JUROBN why store the popularities in their own variable if you have the data already?
        for score in USERS[_id]['popularity']:
            AVG_POP.append(score)
        data.append([_person, _song_count, _total_time, _pop])
    return(data)


def total_mins():
    _total_time = 0
    for _id in UNIQUE_IDS:
        _total_time += USERS[_id]['total_time']
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
