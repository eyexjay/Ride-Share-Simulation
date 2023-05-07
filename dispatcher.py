"""Dispatcher for the simulation"""

from typing import Optional
from driver import Driver
from passenger import Passenger


class Dispatcher:
    """A dispatcher fulfills requests from passengers and drivers for a
    ride-sharing service.

    When a passenger requests a driver, the dispatcher assigns a driver to the
    passenger. If no driver is available, the passenger is placed on a waiting
    list for the next available driver. A passenger that has not yet been
    picked up by a driver may cancel their request.

    When a driver requests a passenger, the dispatcher assigns a passenger from
    the waiting list to the driver. If there is no passenger on the waiting list
    the dispatcher does nothing. Once a driver requests a passenger, the driver
    is registered with the dispatcher, and will be used to fulfill future
    passenger requests.

    === Private Attributes ===
    _drivers:
        A dictionary whose key is driver.id, and value is the driver
    _waiting_passengers:
        A list of passengers waiting to be assigned a driver.
    """

    _drivers: dict[str, Driver]
    _waiting_passengers: list[Passenger]

    def __init__(self) -> None:
        """Initialize a Dispatcher.

        """
        self._drivers = {}
        self._waiting_passengers = []

    def __str__(self) -> str:  # represntation of what
        """Return a string representation.

        """
        return f"Drivers: {self._drivers},/n Waiting Passengers: " \
               f"{self._waiting_passengers} "

    def request_driver(self, passenger: Passenger) -> Optional[Driver]:
        """Return a driver for the passenger, or None if no driver is available.

        Add the passenger to the waiting list if there is no available driver.

        """
        idle_drivers = []
        for driver in self._drivers.values():
            if driver.is_idle:
                idle_drivers.append(driver)

        if not idle_drivers:
            self._waiting_passengers.append(passenger)
            return None
        elif len(idle_drivers) == 1:
            idle_drivers[0].is_idle = False
            return idle_drivers[0]
        else:
            fastest_driver = idle_drivers.pop(0)
            fastest_time = fastest_driver.get_travel_time(passenger.origin)
            for driver in idle_drivers:
                time = driver.get_travel_time(passenger.origin)
                if time < fastest_time:
                    fastest_time = time
                    fastest_driver = driver
            fastest_driver.is_idle = False
            return fastest_driver

    def request_passenger(self, driver: Driver) -> Optional[Passenger]:
        """Return a passenger for the driver, or None if no passenger is
        available.

        If this is a new driver, register the driver for future passenger
        requests.
        """
        if driver.id not in self._drivers:
            self._drivers[driver.id] = driver

        if self._waiting_passengers:
            passenger = self._waiting_passengers.pop(0)
            return passenger
        return None

    def cancel_ride(self, passenger: Passenger) -> None:
        """Cancel the ride for passenger.
        """
        if passenger in self._waiting_passengers:
            self._waiting_passengers.remove(passenger)
        return None


if __name__ == '__main__':
    import python_ta

    python_ta.check_all(
        config={'extra-imports': ['typing', 'driver', 'passenger']})
