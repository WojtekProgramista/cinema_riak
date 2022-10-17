import riak
from src.system import System
from src.functionalities import print_break
from src.stress_tests import test_1, test_2, test_3
import sys

if __name__ == '__main__':
    db_client = riak.RiakClient(pb_port=8087)

    if "--stress-test-1" in sys.argv:
        print ("STRESS TEST 1 IS RUNNING...")
        test_1(System(db_client, screenings_number=32), actions=1000)
        sys.exit("STRESS TEST 1 ENDED")
    elif "--stress-test-2" in sys.argv:
        print ("STRESS TEST 2 IS RUNNING...")
        test_2(System(db_client, screenings_number=32), actions=1000)
        sys.exit("STRESS TEST 2 ENDED")
    elif "--stress-test-3" in sys.argv:
        print ("STRESS TEST 3 IS RUNNING...")
        test_3(System(db_client, screenings_number=32))
        sys.exit("STRESS TEST 3 ENDED")
    elif "--no-clean" in sys.argv:
        system = System(db_client, clean=False)
    else:
        system = System(db_client)

    while True:

        # Main menu
        print_break()

        if system.logged_in_user.is_logged():
            print("1) Make reservation")
            print("2) Log out")

        else:
            print("1) Create new user")
            print("2) Log in")
            print("3) Quit")

        choice = raw_input("\nSelect option (number): ").strip()

        # Make reservation option
        if choice == '1' and system.logged_in_user.is_logged():
            system.make_reservation()

        # Create new user option
        elif choice == '1' and not system.logged_in_user.is_logged():
            system.create_user()

        # Log in option
        elif choice == '2' and not system.logged_in_user.is_logged():
            system.log_in()

        # Log out option
        elif choice == '2' and system.logged_in_user.is_logged():
            system.log_out()

        elif choice == '3' and not system.logged_in_user.is_logged():
            system.quit()
            break
        else:
            print("\nChoose a number from the list.")
