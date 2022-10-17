def print_break():
    print('\n' + '=' * 128 + '\n')


class LoggedInUser:
    def __init__(self, user_dic=None):
        if user_dic is None:
            self.login = None
            self.password = None
            self.reservations = None
            self.logged_in = False
        else:
            self.login = user_dic['login']
            self.password = user_dic['password']
            self.reservations = user_dic['reservations']
            self.logged_in = True

    def is_logged(self):
        return self.logged_in

    def get_login(self):
        return self.login

    def as_dic(self):
        return {
            'login': self.login,
            'password': self.password,
            'reservations': self.reservations,
            'logged_in': self.logged_in
        }