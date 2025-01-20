import random

class Route():
    "Create a train trajectory within a given timeframe"
    def __init__(self, stations: list, max_duration: int):
        """
        Stations is een list die per station de omliggende buren
        en reistijd bevat.
        """
        self.stations = stations
        self.max_duration = max_duration
        self.route = []
        self.travel_time = 0

    def get_neighbours(self, station):
        return station.neighbours

    def is_valid(self, spent_time):
        if spent_time > self.max_duration:
            return False
        else:
            return True

    def add_station(self, station):
        self.route.append(station)
        return self.route

    def get_possible_start(self):
        start_stations = []
        for station in self.stations:
            if len(station.neighbours) == 1:
                start_stations.append(station)
        return start_stations

    def total_travel_time(self):
        return self.travel_time


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
