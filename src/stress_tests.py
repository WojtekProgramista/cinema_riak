import numpy as np
from threading import Thread


# stress test 1

def test_1(system, actions=1000):
    user_dic = {
        'login': "TEST1",
        'password': 'password',
        'reservations': [],
        'logged_in': True
    }

    system.user.bucket.new("TEST1", user_dic).store()

    # User rapidly makes random reservation
    for _ in range(actions):
        if len(user_dic['reservations']) == len(system.reservation.get_keys()):
            print("\nNo more reservations available\n")
            return

        screening_keys = system.screening.get_keys()
        random_screening_key = np.random.choice(screening_keys)
        random_screening_dic = system.screening.select(random_screening_key).data

        available_reservations = random_screening_dic['available_reservations']
        if len(available_reservations) == 0:
            continue
        random_reservation_key = np.random.choice(available_reservations)
        random_reservation_dic = system.reservation.select(random_reservation_key).data

        # update screening available reservations
        random_screening_dic['available_reservations'].remove(random_reservation_key)
        system.screening.update(random_screening_dic)

        # update reservation owner
        random_reservation_dic['owner'] = user_dic['login']
        system.reservation.update(random_reservation_dic)

        # update user reservations
        user_dic['reservations'].append(random_reservation_key)
        system.user.update(user_dic)


# stress test 2

def test_2_thread(system, user_dic, actions):
    for _ in range(actions):
        choice = np.random.choice(["reserve", "reserve"])

        if choice == "reserve":
            screening_keys = system.screening.get_keys()
            random_screening_key = np.random.choice(screening_keys)
            random_screening_dic = system.screening.select(random_screening_key).data

            available_reservations = random_screening_dic['available_reservations']
            if len(available_reservations) == 0:
                continue
            random_reservation_key = np.random.choice(available_reservations)
            random_reservation_dic = system.reservation.select(random_reservation_key).data

            # update screening available reservations
            random_screening_dic['available_reservations'].remove(random_reservation_key)
            system.screening.update(random_screening_dic)

            # update reservation owner
            random_reservation_dic['owner'] = user_dic['login']
            system.reservation.update(random_reservation_dic)

            # update user reservations
            user_dic['reservations'].append(random_reservation_key)
            system.user.update(user_dic)

        else:  # log out and log in
            user_dic['logged_in'] = False
            system.user.update(user_dic)

            user_dic['logged_in'] = True
            system.user.update(user_dic)


def test_2(system, actions=1000):
    user_dic_1 = {
        'login': "TEST2_1",
        'password': "password",
        'reservations': [],
        'logged_in': True
    }
    user_dic_2 = {
        'login': "TEST2_2",
        'password': "password",
        'reservations': [],
        'logged_in': True
    }

    system.user.bucket.new("TEST2_1", user_dic_1).store()
    system.user.bucket.new("TEST2_2", user_dic_2).store()

    Thread(target=test_2_thread(system, user_dic_1, actions)).start()
    Thread(target=test_2_thread(system, user_dic_2, actions)).start()


# stress test 3

def test_3_thread(system, user_dic):
    reservation_keys = system.reservation.get_keys()
    for key in reservation_keys:
        reservation = system.reservation.select(key)
        reservation_dic = reservation.data
        if reservation_dic['owner'] is None:
            reservation_dic['owner'] = user_dic['login']
            system.reservation.update(reservation_dic)

            user_dic['reservations'].append(reservation_dic['id'])
            system.user.update(user_dic)


def test_3(system):
    user_dic_1 = {
        'login': "TEST3_1",
        'password': "password",
        'reservations': [],
        'logged_in': True
    }
    user_dic_2 = {
        'login': "TEST3_2",
        'password': "password",
        'reservations': [],
        'logged_in': True
    }

    system.user.bucket.new("TEST3_1", user_dic_1).store()
    system.user.bucket.new("TEST3_2", user_dic_2).store()

    Thread(target=test_3_thread(system, user_dic_1)).start()
    Thread(target=test_3_thread(system, user_dic_2)).start()
