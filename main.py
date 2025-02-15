import data
from datetime import datetime
import sqlalchemy

SQLITE_URI = "sqlite:///data/flights.sqlite3"
IATA_LENGTH = 3


def delayed_flights_by_airline(data_manager):
    """
    Prompts the user for an airline name and retrieves delayed flights
    for that airline from the database.

    :param data_manager: Instance of FlightData class.
    """
    airline_input = input("Enter airline name: ")
    results = data_manager.get_delayed_flights_by_airline(airline_input)
    print_results(results)


def delayed_flights_by_airport(data_manager):
    """
    Prompts the user for an IATA airport code (validates input),
    then retrieves delayed flights from that airport.

    :param data_manager: Instance of FlightData class.
    """
    while True:
        airport_input = input("Enter origin airport IATA code: ").upper()
        if airport_input.isalpha() and len(airport_input) == IATA_LENGTH:
            break
        print("Invalid IATA code. Try again.")

    results = data_manager.get_delayed_flights_by_airport(airport_input)
    print_results(results)


def flight_by_id(data_manager):
    """
    Prompts the user for a flight ID, validates input, and retrieves
    flight details from the database.

    :param data_manager: Instance of FlightData class.
    """
    while True:
        try:
            flight_id = int(input("Enter flight ID: "))
            break
        except ValueError:
            print("Invalid input. Please enter a numeric flight ID.")

    results = data_manager.get_flight_by_id(flight_id)
    print_results(results)


def flights_by_date(data_manager):
    """
    Prompts the user for a date, validates input format, and retrieves
    flights scheduled for that date.

    :param data_manager: Instance of FlightData class.
    """
    while True:
        try:
            date_input = input("Enter date in DD/MM/YYYY format: ")
            date = datetime.strptime(date_input, "%d/%m/%Y")
            break
        except ValueError:
            print("Invalid format. Please use DD/MM/YYYY format.")

    results = data_manager.get_flights_by_date(date.day, date.month, date.year)
    print_results(results)


def print_results(results):
    """
    Prints the retrieved flight results in a structured format.

    :param results: List of results from a database query.
    """
    print(f"Got {len(results)} results.")
    for result in results:
        result = result._mapping

        try:
            delay = int(result["DEPARTURE_DELAY"]) if result["DEPARTURE_DELAY"] else 0
            origin = result["ORIGIN_AIRPORT"]
            dest = result["DESTINATION_AIRPORT"]
            airline = result["AIRLINE"]
        except (ValueError, sqlalchemy.exc.SQLAlchemyError) as e:
            print("Error showing results: ", e)
            return

        if delay and delay > 0:
            print(
                f"{result['ID']}. {origin} -> {dest} by {airline}, Delay: {delay} Minutes"
            )
        else:
            print(f"{result['ID']}. {origin} -> {dest} by {airline}")


def show_menu_and_get_input():
    """
    Displays the menu and gets user input. If input is valid, returns
    the corresponding function pointer.

    :return: Function to execute.
    """
    print("\nMenu:")
    for key, value in FUNCTIONS.items():
        print(f"{key}. {value[1]}")

    while True:
        try:
            choice = int(input("Select an option: "))
            if choice in FUNCTIONS:
                return FUNCTIONS[choice][0]
        except ValueError:
            pass
        print("Invalid choice. Try again.")


# Menu options mapping
FUNCTIONS = {
    1: (flight_by_id, "Show flight by ID"),
    2: (flights_by_date, "Show flights by date"),
    3: (delayed_flights_by_airline, "Delayed flights by airline"),
    4: (delayed_flights_by_airport, "Delayed flights by origin airport"),
    5: (quit, "Exit"),
}


def main():
    """
    Main function that initializes the data manager and loops through
    menu options until the user exits.
    """
    data_manager = data.FlightData(SQLITE_URI)

    while True:
        choice_func = show_menu_and_get_input()
        choice_func(data_manager)


if __name__ == "__main__":
    main()
