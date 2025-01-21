import random

class Route():
    "Create a train trajectory within a given timeframe"
    def __init__(self, stations: list, max_duration: int):
        """
        Stations is een list die per station de omliggende buren
        en reistijd bevat.
        """
        self.stations = stations
        self.start_stations = []
        self.max_duration = max_duration
        self.route = []
        self.travel_time = 0

    def get_neighbours(self, station):
        return station.neighbours

    def is_valid(self, spent_time):
        if spent_time > self.max_duration:
            return False
        return True

    def add_station(self, station, travel_time=0):
        self.route.append(station)
        self.travel_time += travel_time
        return self.route

    def get_possible_start(self):
        for station in self.stations:
            if len(station.neighbours) == 1:
                self.start_stations.append(station)
        return self.start_stations

    def pick_start(self):
        if random.random() < 0.5:
            current_station = random.choice(self.start_stations)
        else:
            current_station = random.choice(self.stations)
        return current_station

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
