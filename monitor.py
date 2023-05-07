"""
The Monitor module contains the Monitor class, the Activity class,
and a collection of constants. Together the elements of the module
help keep a record of activities that have occurred.

Activities fall into two categories: Passenger activities and Driver
activities. Each activity also has a description, which is one of
request, cancel, pickup, or dropoff.

=== Constants ===
PASSENGER: A constant used for the Passenger activity category.
DRIVER: A constant used for the Driver activity category.
REQUEST: A constant used for the request activity description.
CANCEL: A constant used for the cancel activity description.
PICKUP: A constant used for the pickup activity description.
DROPOFF: A constant used for the dropoff activity description.
"""

from typing import Dict, List
from location import Location, \
    manhattan_distance  # i added the comma and manhattan_distance part

PASSENGER = "passenger"
DRIVER = "driver"

REQUEST = "request"
CANCEL = "cancel"
PICKUP = "pickup"
DROPOFF = "dropoff"


class Activity:
    """An activity that occurs in the simulation.

    === Attributes ===
    timestamp: The time at which the activity occurred.
    description: A description of the activity.
    identifier: An identifier for the person doing the activity.
    location: The location at which the activity occurred.
    """

    time: int
    description: str
    id: str
    location: Location

    def __init__(self, timestamp: int, description: str, identifier: str,
                 location: Location) -> None:
        """Initialize an Activity.

        """
        self.time = timestamp
        self.description = description
        self.id = identifier
        self.location = location


class Monitor:
    """A monitor keeps a record of activities that it is notified about.
    When required, it generates a report of the activities it has recorded.
    """

    # === Private Attributes ===
    _activities: Dict[str, Dict[str, List[Activity]]]

    #       A dictionary whose key is a category, and value is another
    #       dictionary. The key of the second dictionary is an identifier
    #       and its value is a list of Activities.

    def __init__(self) -> None:
        """Initialize a Monitor.

        """
        self._activities = {
            PASSENGER: {},
            DRIVER: {}
        }
        """@type _activities: dict[str, dict[str, list[Activity]]]"""

    def __str__(self) -> str:
        """Return a string representation.

        """
        return f"Monitor ({len(self._activities[DRIVER])} drivers, " \
               f"{len(self._activities[PASSENGER])} passengers)"

    def notify(self, timestamp: int, category: str, description: str,
               identifier: str, location: Location) -> None:
        """Notify the monitor of the activity.

        timestamp: The time of the activity.
        category: The category (DRIVER or PASSENGER) for the activity.
        description: A description (REQUEST | CANCEL | PICKUP | DROPOFF)
            of the activity.
        identifier: The identifier for the actor.
        location: The location of the activity.
        """
        if identifier not in self._activities[category]:
            self._activities[category][identifier] = []

        activity = Activity(timestamp, description, identifier, location)
        self._activities[category][identifier].append(activity)

    def report(self) -> Dict[str, float]:
        """Return a report of the activities that have occurred.

        """
        return {"average_passenger_wait_time": self._average_wait_time(),
                "average_driver_total_distance": self._average_total_distance(),
                "average_driver_trip_distance": self._average_trip_distance()}

    def _average_wait_time(self) -> float:
        """Return the average wait time of passengers that have either been
         picked up or have cancelled their trip.

        """
        wait_time = 0
        count = 0
        for activities in self._activities[PASSENGER].values():
            # A passenger that has less than two activities hasn't finished
            # waiting (they haven't cancelled or been picked up).
            if len(activities) >= 2:
                # The first activity is REQUEST, and the second is PICKUP
                # or CANCEL. The wait time is the difference between the two.
                wait_time += activities[1].time - activities[0].time
                count += 1
        return wait_time / count

    def _average_total_distance(self) -> float:
        """Return the average distance drivers have driven.

        """
        total_distance = 0
        driver_activity = self._activities[DRIVER]
        for driver_id in driver_activity:
            for index in range(len(driver_activity[driver_id]) - 1):
                start_location = driver_activity[driver_id][index].location
                end_location = driver_activity[driver_id][index + 1].location
                total_distance += manhattan_distance(start_location,
                                                     end_location)
        return total_distance / len(driver_activity)

    def _average_trip_distance(self) -> float:
        """Return the average distance drivers have driven on trips.

        """
        total_distance = 0
        driver_activity = self._activities[DRIVER]
        for driver_id in driver_activity:
            for index in range(len(driver_activity[driver_id]) - 1):
                start_activity = driver_activity[driver_id][index]
                end_activity = driver_activity[driver_id][index + 1]
                if start_activity.description == PICKUP and \
                        end_activity.description == DROPOFF:
                    total_distance += manhattan_distance(
                        start_activity.location, end_activity.location)
        return total_distance / len(driver_activity)


if __name__ == "__main__":
    import python_ta

    python_ta.check_all(
        config={
            'max-args': 6,
            'extra-imports': ['typing', 'location']})
