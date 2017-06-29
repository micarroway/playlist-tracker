from User import User


class Users(dict):
    def __init__(self):
        self.num_tracks = 0
        dict.__init__(self)

    def __setitem__(self, key, value):
        if not isinstance(value, User):
            raise NotImplementedError

        dict.__setitem__(self, key, value)

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
