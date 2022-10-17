import riak
from src.db_objects import User, Reservation, Screening
from src.functionalities import LoggedInUser, print_break


class System:
    def clear(self):
        for db_object in [self.user, self.reservation, self.screening]:
            keys = db_object.get_keys()
            for key in keys:
                db_object.delete(key)

    def create_screenings(self, n):
        available_screening_rooms = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        available_times = ["16:00", "19:00", "22:00"]
        available_titles = ["Matrix", "Dune", "Harry Potter", "Star Wars", "Indiana Jones", "The Room"]

        for i in range(n):
            available_reservations = []

            count = 0
            for row in range(8):
                for seat in range(8):
                    reservation_id = str(i) + "-" + str(count)

                    _, escape = self.reservation.create({
                        'id': reservation_id,
                        'screening_id': str(i),
                        'row': row + 1,
                        'seat': seat + 1,
                        'owner': None
                    })
                    count += 1
                    assert escape

                    available_reservations.append(reservation_id)

            title = available_titles[i % 6]
            screening_room = available_screening_rooms[i % 9]
            time = available_times[i % 3]

            screening_dic = {
                'id': str(i),
                'title': title,
                'screening_room': screening_room,
                'available_reservations': available_reservations,
                'time': time
            }

            _, escape = self.screening.create(screening_dic)
            assert escape

    def __init__(self, client, clean=True, screenings_number=3):
        self.user = User(client)
        self.reservation = Reservation(client)
        self.screening = Screening(client)

        self.logged_in_user = LoggedInUser()

        if clean:
            self.clear()
            self.create_screenings(screenings_number)

    def log_in(self):
        print_break()
        login = raw_input("Type login: ").strip()
        password = raw_input("Type password: ").strip()

        try:
            fetched_user = self.user.select(login)
            if fetched_user.data['logged_in']:
                msg, escape = "User is already logged in in other session. Log out from that session first.", False
            elif fetched_user.data['password'] != password:
                msg, escape = "Wrong login or password.", False
            else:
                self.logged_in_user = LoggedInUser(fetched_user.data)
                self.user.update(self.logged_in_user.as_dic())
                msg, escape = "Welcome {}!".format(fetched_user.data['login']), True

        except (riak.riak_error.RiakError, TypeError):
            msg, escape = "Wrong login or password.", False

        except ValueError as e:
            msg, _ = "One or more values are missing. Enter login and password.", False

        print_break()
        print("{}".format(msg))

    def log_out(self):
        while True:
            print_break()
            try:
                self.logged_in_user.logged_in = False
                self.user.update(self.logged_in_user.as_dic())
                self.logged_in_user = LoggedInUser()
                msg, escape = "You logged out from the system.", True
            except riak.riak_error.RiakError:
                msg, escape = "Something went wrong, please try again.", False

            print(msg)
            if escape:
                break

    def make_reservation(self):
        while True:
            print_break()
            keys = self.screening.get_keys()

            for i, key in enumerate(keys):
                curr_screening = self.screening.select(key).data
                print(str(i + 1) + ") " + curr_screening['title'])
                print("(time: {}, screening room: {})\n"
                      .format(curr_screening['time'], curr_screening['screening_room']))

            choice = raw_input("Select screening (number): ").strip()

            if choice.isdigit() and 0 < int(choice) <= len(keys):
                selected_screening = self.screening.select(keys[int(choice) - 1])

                msg = "Choose an unoccupied seat (screen is at the top)\n"
                while True:
                    print_break()
                    selected_screening.reload()
                    selected_screening_dic = selected_screening.data
                    print("Chosen movie: {}\n".format(selected_screening_dic['title']))

                    room_matrix = [["OCCUPIED  " for _ in range(8)] for _ in range(8)]
                    available_reservations = selected_screening_dic['available_reservations']

                    if len(available_reservations) == 0:
                        print("\nAll seats for this screening are occupied.")
                        return

                    for reservation_key in available_reservations:
                        reservation_dic = self.reservation.select(reservation_key).data
                        row, seat = reservation_dic['row'], reservation_dic['seat']
                        room_matrix[row - 1][seat - 1] = "ROW: " + str(row) + ", S: " + str(seat)

                    print("-" * 128)
                    for row in range(8):
                        print(("| {: >12} |" * 8).format(*room_matrix[row]))
                        print("-" * 128)

                    print("\n" + msg)

                    row = raw_input("Select row (number): ").strip()
                    seat = raw_input("Select seat [S] (number): ").strip()

                    chosen_reservation_key = None
                    chosen_reservation_dic = None
                    for j, reservation_key in enumerate(available_reservations):
                        chosen_reservation_dic = self.reservation.select(reservation_key).data
                        if chosen_reservation_dic['owner'] is not None:
                            break

                        if str(chosen_reservation_dic['row']) == row and str(chosen_reservation_dic['seat']) == seat:
                            chosen_reservation_key = available_reservations.pop(j)
                            print("test" + chosen_reservation_key)

                            # update screening available reservations
                            selected_screening_dic['available_reservations'] = available_reservations
                            self.screening.update(selected_screening_dic)

                            # update reservation owner
                            chosen_reservation_dic['owner'] = self.logged_in_user.get_login()
                            self.reservation.update(chosen_reservation_dic)

                            # update user reservations
                            self.logged_in_user.reservations.append(chosen_reservation_key)
                            self.user.update(self.logged_in_user.as_dic())

                            break

                    if chosen_reservation_key is None:
                        msg = "Try again. Remember to choose from unoccupied seats.\n"
                    else:
                        print_break()
                        print("You successfully made a reservation.")
                        print("Reservation details:")
                        print("Movie title: {}".format(selected_screening_dic['title']))
                        print("Time: {}".format(selected_screening_dic['time']))
                        print("Room: {}".format(selected_screening_dic['screening_room']))
                        print("Row: {}".format(chosen_reservation_dic['row']))
                        print("Seat number: {}".format(chosen_reservation_dic['seat']))
                        break
                break

            else:
                print("\nChoose a number from the list.")

    def create_user(self):

        while True:
            print_break()
            login = raw_input("Type login: ").strip()
            password = raw_input("Type password: ").strip()
            msg, escape = self.user.create({
                'login': login,
                'password': password,
                'reservations': [],
                'logged_in': False
            })

            print("\n{}".format(msg))
            if escape:
                break

    def quit(self):
        print_break()
        print("Good bye.")
