from os import linesep

from PlaylistTracker.User import User


class Users(dict):
    __slots__ = ['allowed_minutes', 'num_tracks']
    
    def __init__(self, **kwargs):
        self.allowed_minutes = kwargs['allowed_minutes'] if 'allowed_minutes' in kwargs.keys() else 0
        self.num_tracks = 0        

    def __init__(self, **kwargs):
        self.allowed_minutes = kwargs['allowed_minutes'] if 'allowed_minutes' in kwargs.keys() else 0
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
        string_value += '  ' + ('-' * 66) + linesep
        total_minutes = self.get_total_minutes()
        string_value += '%s%s songs, %s mins, %s Avg Popularity' % (
            (' ' * 22),
            str(self.num_tracks).rjust(3),
            str(round(total_minutes, 2)).rjust(7),
            str(round(self.get_average_popularity(), 2)).rjust(5)) + linesep

        limit = round(self.allowed_minutes - total_minutes)
        per_person_time_limit = self.allowed_minutes / len(sorted_users)

        string_value += linesep

        if total_minutes > self.allowed_minutes:
            string_value += '      The total time is over the limit by %s mins.' % (limit * -1) + linesep
        elif total_minutes == self.allowed_minutes:
            string_value += '      The total time is at the limit.' + linesep
        else:
            string_value += '      The total time is under the limit by %s mins.' % limit + linesep

        for user in sorted_users:
            user_time = float(user.get_total_minutes())
            if user_time > per_person_time_limit:
                overage = str(round(user_time - per_person_time_limit))
                string_value += '%s is %s the limit by %s mins.' % (user.display_name.rjust(20),
                                                                    'over'.rjust(5),
                                                                    overage.rjust(3)) + linesep
            if user_time < per_person_time_limit:
                remainder = str(round(user_time - per_person_time_limit) * -1)
                string_value += '%s is %s the limit by %s mins.' % (user.display_name.rjust(20),
                                                                    'under'.rjust(5),
                                                                    remainder.rjust(3)) + linesep
            if user_time == per_person_time_limit:
                string_value +=  '%s is at the limit.' % (user.display_name.rjust(20))

        return string_value + linesep

    def get_total_minutes(self):
        return sum(user.get_total_minutes() for user in self.values())

    def get_average_popularity(self):
        return sum(user.popularity for user in self.values()) / self.num_tracks

    def add_track(self, user_id, track):
        if user_id not in self:
            raise IndexError

        self.num_tracks += 1
        self[user_id].add_track(track)
