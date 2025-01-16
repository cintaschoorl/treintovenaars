import random

class Route():
    "Create a train trajectory within a given timeframe"
    def __init__(self, stations: dict, max_duration: int):
        """
        Neighbours is een dict die per station de omliggende buren
        en reistijd bevat.
        """
        self.stations = stations
        self.max_duration = max_duration
        self.route = []

    def get_neighbours(self, current_station):
        neighbour_station = self.stations[current_station].get('neighbours', {})
        next_station, travel_time = random.choice(list(neighbour_station.items()))
        return next_station, travel_time

    def is_valid(self, spent_time):
        if spent_time > self.max_duration:
            return False
        else:
            return True

    def add_station(self, next_station):
        self.route.append(next_station)
        return self.route



stations = {
    "slo": {
        "name": "Amsterdam Sloterdijk",
        "coordinates": (52.3881, 4.8372),
        "neighbours": {
            "haa": 10,
            "zaa": 12,
        },
    },
    "haa": {
        "name": "Haarlem",
        "coordinates": (52.3874, 4.6462),
        "neighbours": {
            "slo": 10,
            "zaa": 8,
        },
    },
    "zaa": {
        "name": "Zaandam",
        "coordinates": (52.4381, 4.8245),
        "neighbours": {
            "haa": 8,
            "slo": 12,
        },
    },
    "acs": {
        "name": "Amsterdam Centraal",
        "coordinates": (52.3784, 4.9003),
        "neighbours": {
            "slo": 5,
        },
    },
}

spent_time = 50
start_station = 'slo'
route = Route(stations, max_duration=120)
route.add_station(start_station)
next_station, travel_time = route.get_neighbours(start_station)
spent_time += travel_time
if route.is_valid(spent_time) == True:
    whole_route = route.add_station(next_station)
start_station = next_station
print(whole_route)






    # def add_name(self, train_name):
    #     self.id = train_name

#    def add_connection(self, station1, station2):
#        """
#        Voegt connecties aan traject toe.
#        """
#        for c in self.connection_list:
#            # search right connection
#            if c.station1 == station1 and c.station2 == station2:
                # check if within timeframe
#                if (self.duration + c.travel_time) < self.max_duration:
#                    if self.traject == []:

#                    self.traject.append(c.station1)
#                        self.traject.append(c.station2)
#                    else:
                        # add only the second
#                        self.traject.append(c.station2)

#                    self.duration += c.travel_time
#                    print(f"Connection {station1} - {station2} added: total duration is {self.duration} min.")

#                else:
#                    print(f"Max duration of {self.max_duration} min exceeded.")
