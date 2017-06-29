from User import User


class Users(dict):
    def get_average_popularity(self):
        return 1

    def get_total_minutes(self):
        total_minutes = 0
        for x in self.values():
            if not isinstance(x, User):
                return NotImplementedError
            total_minutes += x.get_total_minutes()

        return total_minutes
