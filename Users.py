from User import User

from os import linesep


class Users(dict):
    def __init__(self):
        self.allowed_minutes = 0
        self.num_tracks = 0
        dict.__init__(self)

    def __setitem__(self, key, value):
        if not isinstance(value, User):
            raise NotImplementedError

        dict.__setitem__(self, key, value)

    def __str__(self):
        sorted_users = sorted(self.values(), key=lambda u: str.lower(u.display_name))
        string_value = linesep
        for user in sorted_users:
            string_value += str(user) + linesep
        string_value += '--------------------------------------------------------' + linesep
        string_value += '%s songs, %s mins, %s Avg Popularity' % (
            self.num_tracks,
            self.get_total_minutes(),
            self.get_average_popularity()
        ) + linesep

        total_minutes = self.get_total_minutes()
        limit = round(self.allowed_minutes - self.get_total_minutes())
        per_person_time_limit = self.allowed_minutes / len(sorted_users)

        string_value += linesep

        if total_minutes > self.allowed_minutes:
            string_value += 'The total time is over the limit by %s mins.' % (limit * -1) + linesep
        elif total_minutes == self.allowed_minutes:
            string_value += 'Good job, guys.' + linesep
        else:
            string_value += 'The total time is under the limit by %s mins.' % limit + linesep

        for user in sorted_users:
            user_time = float(user.get_total_minutes())
            if user_time > per_person_time_limit:
                overage = str(round(user_time - per_person_time_limit))
                string_value += '%s is over the limit by %s mins.' % (user.display_name,
                                                                      overage) + linesep
            if user_time < per_person_time_limit:
                under = str(round(user_time - per_person_time_limit) * -1)
                string_value += '%s is under the limit by %s mins.' % (user.display_name,
                                                                       under) + linesep

        return string_value + linesep

    def get_total_minutes(self):
        total_minutes = 0
        for user in self.values():
            # if not isinstance(x, User):
            #     return NotImplementedError
            total_minutes += user.get_total_minutes()

        return round(total_minutes, 2)

    def get_average_popularity(self):
        total_popularity = 0
        total_song_count = 0
        for user in self.values():
            total_popularity += user.popularity
            total_song_count += user.song_count

        if total_song_count == 0:
            return 0

        return round(total_popularity / total_song_count, 2)

    def add_track(self, user_id, track):
        if user_id not in self:
            raise IndexError

        self.num_tracks += 1
        self[user_id].add_track(track)
