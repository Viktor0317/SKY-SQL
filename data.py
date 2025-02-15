from sqlalchemy import create_engine, text


class FlightData:
    """A class for interacting with the flight database."""

    def __init__(self, db_uri):
        """
        Initializes the database connection.

        :param db_uri: Database connection URI.
        """
        self.engine = create_engine(db_uri)

    def _execute_query(self, query, params=None):
        """
        Executes a SQL query and fetches all results.

        :param query: The SQL query to execute.
        :param params: Dictionary of query parameters.
        :return: List of query results.
        """
        if params is None:
            params = {}
        with self.engine.connect() as connection:
            result = connection.execute(text(query), params)
            return result.fetchall()

    def get_flight_by_id(self, flight_id):
        """
        Retrieves flight details based on flight ID.

        :param flight_id: The ID of the flight.
        :return: Flight details.
        """
        query = """
        SELECT flights.ID, flights.ORIGIN_AIRPORT, flights.DESTINATION_AIRPORT, 
               airlines.AIRLINE, flights.DEPARTURE_DELAY 
        FROM flights
        JOIN airlines ON flights.AIRLINE = airlines.ID
        WHERE flights.ID = :flight_id
        """
        return self._execute_query(query, {"flight_id": flight_id})

    def get_flights_by_date(self, day, month, year):
        """
        Retrieves flights scheduled for a specific date.

        :param day: The day of the flight.
        :param month: The month of the flight.
        :param year: The year of the flight.
        :return: List of flights on the given date.
        """
        query = """
        SELECT flights.ID, flights.ORIGIN_AIRPORT, flights.DESTINATION_AIRPORT, 
               airlines.AIRLINE, flights.DEPARTURE_DELAY 
        FROM flights
        JOIN airlines ON flights.AIRLINE = airlines.ID
        WHERE flights.YEAR = :year 
          AND flights.MONTH = :month 
          AND flights.DAY = :day
        """
        return self._execute_query(query, {"day": day, "month": month, "year": year})

    def get_delayed_flights_by_airline(self, airline_name):
        """
        Retrieves delayed flights for a specific airline.

        A flight is considered delayed if its departure delay is 20 minutes or more.

        :param airline_name: The airline name.
        :return: List of delayed flights for the airline.
        """
        query = """
        SELECT flights.ID, flights.ORIGIN_AIRPORT, flights.DESTINATION_AIRPORT, 
               airlines.AIRLINE, flights.DEPARTURE_DELAY 
        FROM flights
        JOIN airlines ON flights.AIRLINE = airlines.ID
        WHERE airlines.AIRLINE = :airline_name 
          AND flights.DEPARTURE_DELAY >= 20
        ORDER BY flights.DEPARTURE_DELAY DESC
        """
        return self._execute_query(query, {"airline_name": airline_name})

    def get_delayed_flights_by_airport(self, airport_code):
        """
        Retrieves delayed flights departing from a specific airport.

        A flight is considered delayed if its departure delay is 20 minutes or more.

        :param airport_code: The IATA code of the origin airport.
        :return: List of delayed flights from the airport.
        """
        query = """
        SELECT flights.ID, flights.ORIGIN_AIRPORT, flights.DESTINATION_AIRPORT, 
               airlines.AIRLINE, flights.DEPARTURE_DELAY 
        FROM flights
        JOIN airlines ON flights.AIRLINE = airlines.ID
        WHERE flights.ORIGIN_AIRPORT = :airport_code 
          AND flights.DEPARTURE_DELAY >= 20
        ORDER BY flights.DEPARTURE_DELAY DESC
        """
        return self._execute_query(query, {"airport_code": airport_code})
