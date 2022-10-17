from schema import Schema, Or
from schema import SchemaMissingKeyError, SchemaError
import riak
import re


class User:
    def __init__(self, client):
        self.bucket = client.bucket('customer')

    def create(self, user_dic):
        try:
            Schema({
                'login': str,
                'password': str,
                'reservations': lambda x: len(x) == 0,
                'logged_in': Or(True, False)
            }).validate(user_dic)
        except SchemaMissingKeyError as e:
            return e.__str__(), False
        except SchemaError as e:
            return e.__str__(), False

        key, val = user_dic['login'], user_dic

        try:
            self.bucket.new(key, val).store(if_none_match=True)
        except riak.riak_error.RiakError:
            return "Login already taken. Please enter other login.", False
        except ValueError as e:
            return "One or more values are missing.", False

        return "User was successfully created.", True

    def select(self, key):
        return self.bucket.get(key)

    def update(self, user_dic):
        key, val = user_dic['login'], user_dic
        user_object = self.select(key)
        user_object.data = val
        user_object.store()

    def delete(self, key):
        self.select(key).delete()

    def get_keys(self):
        return self.bucket.get_keys()


class Reservation:
    def __init__(self, client):
        self.bucket = client.bucket('reservation')

    def create(self, res_dic):
        try:
            Schema({
                'id': str,
                'screening_id': str,
                'row': int,
                'seat': int,
                'owner': Or(None, str)
            }).validate(res_dic)
        except SchemaMissingKeyError as e:
            return e.__str__(), False
        except SchemaError as e:
            return e.__str__(), False

        key, val = res_dic['id'], res_dic

        try:
            self.bucket.new(key, val).store(if_none_match=True)
        except riak.riak_error.RiakError:
            return "Reservation with the same id already exists.", False
        except ValueError as e:
            return "One or more values are missing.", False

        return "Reservation {} was created successfully".format(key), True

    def select(self, key):
        return self.bucket.get(key)

    def update(self, res_dic):
        key, val = res_dic['id'], res_dic
        user_object = self.select(key)
        user_object.data = val
        user_object.store()

    def delete(self, key):
        self.select(key).delete()

    def get_keys(self):
        return self.bucket.get_keys()


class Screening:
    def __init__(self, client):
        self.bucket = client.bucket('screening')

    def create(self, scr_dic):
        try:
            Schema({
                'id': str,
                'title': str,
                'screening_room': int,
                'available_reservations': lambda x: len(x) == 64,
                'time': lambda x: bool(re.compile(r"^[0-2][0-9]:[0-5][0-9]$").match(x))
            }).validate(scr_dic)
        except SchemaMissingKeyError as e:
            return e.__str__(), False
        except SchemaError as e:
            return e.__str__(), False

        key, val = scr_dic['id'], scr_dic

        try:
            self.bucket.new(key, val).store(if_none_match=True)
        except riak.riak_error.RiakError:
            return "Reservation with the same id already exists.", False
        except ValueError as e:
            return "One or more values are missing.", False

        return "Reservation {} was created successfully".format(key), True

    def select(self, key):
        return self.bucket.get(key)

    def update(self, scr_dic):
        key, val = scr_dic['id'], scr_dic
        user_object = self.select(key)
        user_object.data = val
        user_object.store()

    def delete(self, key):
        self.select(key).delete()

    def get_keys(self):
        return self.bucket.get_keys()
