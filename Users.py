from User import User


class Users(dict):

    def __set_item__(self, key, value):
        print(key)
        dict.__setitem__(self,key,value)

    def get_total_minutes(self):
        total_minutes = 0
        for user in self.values():
            # if not isinstance(x, User):
            #     return NotImplementedError
            total_minutes += user.get_total_minutes()

        return total_minutes

    def get_average_popularity(self):
        total_popularity = 0
        total_song_count = 0
        for user in self.values():
            total_popularity += user.popularity
            total_song_count += user.song_count

        if total_song_count == 0:
            return 0

        return round(total_popularity/total_song_count, 2)