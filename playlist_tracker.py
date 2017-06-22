# -*- coding: utf-8 -*-
"""
Created on Thu Jun 22 09:01:41 2017

@author: JCatoe
"""
import spotipy
import spotipy.util as util
from operator import itemgetter

PORT_NUMBER = 8080
SPOTIPY_CLIENT_ID = '4243669c01eb4b138042f871b5b29dca'
SPOTIPY_CLIENT_SECRET = '2758ef2017a9433f9c078a5af1be981e'
SPOTIPY_REDIRECT_URI = 'http://localhost:8080'

username = 'cptyaimie'
token = util.prompt_for_user_token(username,
                                   scope='playlist-read-collaborative',
                                   client_id=SPOTIPY_CLIENT_ID,
                                   client_secret=SPOTIPY_CLIENT_SECRET,
                                   redirect_uri=SPOTIPY_REDIRECT_URI)

sp = spotipy.Spotify(auth=token)

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
                      'total_time': 0}
         }

USERS_LIST = list(USERS.keys())
UNIQUE_IDS = []
AVG_POP = []
SONGS = []
TOTAL_PEOPLE = len(USERS_LIST)


def ms_to_min(ms):
    x = ms / 1000
    minutes = x / 60
    return(round(minutes, 2))


def is_new_id(test):
    if test in UNIQUE_IDS:
        return(False)
    else:
        return(True)


def get_data(tracks):
    print(tracks)
    for i, item in enumerate(tracks['items']):
        _added_by = item['added_by']['id']
        if is_new_id(_added_by):
            UNIQUE_IDS.append(_added_by)
        SONGS.append(item['track'])
        # update dictionary
        _pop = item['track']['popularity']
        USERS[_added_by]['song_count'] += 1
        USERS[_added_by]['total_time'] += item['track']['duration_ms']
        USERS[_added_by]['popularity'].append(_pop)
    return(total)


def collect_clean_data():
    data = []
    for _id in UNIQUE_IDS:
        _person = USERS[_id]['person']
        _song_count = str(USERS[_id]['song_count'])
        _total_time = str(ms_to_min(USERS[_id]['total_time']))
        _avg = sum(USERS[_id]['popularity']) / len(USERS[_id]['popularity'])
        _pop = str(round(_avg, 2))
        for score in USERS[_id]['popularity']:
            AVG_POP.append(score)
        data.append([_person, _song_count, _total_time, _pop])
    return(data)


def song_counts_match():
    _overall_count = len(SONGS)
    _dict_count = 0
    for _id in UNIQUE_IDS:
        _dict_count += USERS[_id]['song_count']
    if _overall_count != _dict_count:
        print('MISSING SOMEONE')
        return(False)
    else:
        return(True)


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
    _limit = round(720 - total_time)
    _per_person_limit = 720 / 6

    if total_time > 720:
        print('The total time is over the limit by %s mins.' % (_limit*-1))
    elif total_time == 720:
        print('Good job, guys.')
    else:
        print('The total time is under the limit by %s mins.' % _limit)


    for person in data:
        _personal_time = float(person[2])
        if _personal_time > _per_person_limit:
            _overage = str(round(_personal_time - _per_person_limit))
            print(' %s is over the limit by %s mins.' % (person[0].rjust(8),
                                                        _overage))
        if _personal_time < _per_person_limit:
            _under = str(round(_personal_time - _per_person_limit)*-1)
            print(' %s is under the limit by %s mins.' % (person[0].rjust(8),
                                                          _under))


def pprint(data):
    print()
    if song_counts_match():
        for person in data:
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
    all_playlists = sp.user_playlists(username)
    chicago = all_playlists['items'][0]
    owner = chicago['owner']['id']
    results = sp.user_playlist(owner,
                               chicago['id'],
                               fields='tracks,next')
    tracks = results['tracks']
    get_data(tracks)
    while tracks['next']:
        tracks = sp.next(tracks)
        get_data(tracks)

    sort_by = {'person': 0,
               'songs': 1,
               'time': 2,
               'popularity': 3}

    data = sorted(collect_clean_data(),
                  key=itemgetter(sort_by['popularity']),
                  reverse=True)
    pprint(data)
