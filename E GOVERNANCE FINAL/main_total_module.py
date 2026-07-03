"""Government Scheme Eligibility Application."""
from sector import display_sectors
from eligibility import check_eligibility
from application import ApplicationRecord, ApplicationRepository
from schemes import SchemeRepository
from auth import AuthenticationService


def authenticate() -> str:
    """Console login/registration gate. Returns the logged-in username."""
    auth_service = AuthenticationService()

    while True:
        print("\n1. Login")
        print("2. Register")
        choice = input("Enter Choice: ")

        if choice == "1":
            username = input("Username: ")
            password = input("Password: ")
            if auth_service.sign_in(username, password):
                print("Login Successful")
                return username
            print("Invalid Username or Password")

        elif choice == "2":
            username = input("Choose Username: ")
            password = input("Choose Password: ")
            if auth_service.sign_up(username, password):
                print("Registration Successful. Please Login.")
            else:
                print("Username Already Exists Or Invalid Input")

        else:
            print("Invalid Choice")


class SchemeApp:
    """Console application that lets citizens check and apply for schemes."""

    def __init__(self, username: str = "guest"):
        self.username = username
        self.scheme_repo = SchemeRepository()
        self.application_repo = ApplicationRepository()

    @staticmethod
    def read_int(prompt: str) -> int:
        """Reads an int from input, returning -1 on bad input instead of crashing."""
        try:
            return int(input(prompt))
        except ValueError:
            return -1

    @staticmethod
    def collect_citizen_details() -> tuple[str, int, int, str, str]:
        print("\nEnter Citizen Details")
        name = input("Name: ")
        age = int(input("Age: "))
        income = int(input("Annual Income: "))
        occupation = input("Occupation: ")
        gender = input("Gender: ")
        return name, age, income, occupation, gender

    def apply_for_scheme(self, name: str, sector: str, scheme: str) -> None:
        apply_choice = input("Apply for Scheme (yes/no): ")
        if apply_choice.lower() == "yes":
            record = ApplicationRecord(name=name, sector=sector, scheme=scheme, status="Applied")
            self.application_repo.save(record)
            print("Application Saved Successfully")

    def handle_scheme(self, sector: str, scheme: str) -> str:
        """Runs the eligibility + apply flow. Returns 'continue', 'back', 'exit', or 'invalid'."""
        name, age, income, occupation, gender = self.collect_citizen_details()
        rules = self.scheme_repo.rules(sector, scheme)
        is_eligible, message = check_eligibility(rules, age, income, occupation, gender)

        if is_eligible:
            print("\nEligible for", scheme)
            self.apply_for_scheme(name, sector, scheme)
        else:
            print("\nNot Eligible")
            print("Reason:", message)

        print("\n1. Apply Another Scheme")
        print("2. Change Sector")
        print("3. Exit")

        option = self.read_int("Enter Choice: ")
        return {1: "continue", 2: "back", 3: "exit"}.get(option, "invalid")

    def scheme_loop(self, sector: str) -> bool:
        """Runs the scheme-selection loop for a sector. Returns False if the app should exit."""
        while True:
            scheme_list = self.scheme_repo.schemes_in(sector)

            print("\nAvailable Schemes")
            for index, name in enumerate(scheme_list, start=1):
                print(index, ".", name)
            print("0. Back")

            choice = self.read_int("\nSelect Scheme: ")

            if choice == 0:
                return True
            if choice < 1 or choice > len(scheme_list):
                print("Invalid Choice")
                continue

            scheme = scheme_list[choice - 1]
            result = self.handle_scheme(sector, scheme)

            if result == "continue":
                continue
            if result == "back":
                return True
            if result == "exit":
                print("Thank You")
                return False
            print("Invalid Choice")

    def run(self) -> None:
        while True:
            sectors = display_sectors()
            print("0. Exit")

            choice = self.read_int("\nSelect Sector: ")

            if choice == 0:
                print("Thank You")
                break
            if choice < 1 or choice > len(sectors):
                print("Invalid Choice")
                continue

            sector = sectors[choice - 1]
            if not self.scheme_loop(sector):
                break


if __name__ == "__main__":
    logged_in_user = authenticate()
    SchemeApp(logged_in_user).run()
