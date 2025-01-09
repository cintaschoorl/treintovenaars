import csv

class Station():
    """
    Represents a train station with a name and coordinates.
    Attributes are: name and y- and x-coordinate.
    """
    def __init__(self,  name, y, x):
        self.name = name
        self.y = y
        self.x = x

    def print(self):
        return f'{self.name}'

class Connection():
    """
    Represents a connection between two train stations with a travel time.
    Attributes are: names and travel time.
    """
    def __init__(self, station1, station2, travel_time):
        self.station1 = station1
        self.station2 = station2
        self.travel_time = travel_time

class Trajectory():
    "Trajectory, yeah"
    def __init__(self, connection_list, max_duration: int):
        self.connection_list = connection_list
        self.max_duration = max_duration

        self.duration = 0
        self.traject = []

        # for c in self.connection_list[:5]:
        #     self.add_connection(c.station1, c.station2)

    def add_connection(self, station1, station2):
        """
        Voegt connecties aan traject toe.
        Nog automatizeren!!!
        """
        for c in self.connection_list:
            # search right connection
            if c.station1 == station1 and c.station2 == station2:
                # check if within timeframe
                if (self.duration + c.travel_time) < self.max_duration:     
                    # add both 1 and 2 if list is empty     
                    if self.traject == []:

                        self.traject.append(c.station1)
                        self.traject.append(c.station2)
                    else:
                        # add only the second
                        self.traject.append(c.station2)

                    self.duration += c.travel_time
                    print(f"Connection {station1} - {station2} added:")
                    print(f"Total trajectory time is: {self.duration} minutes")

                else:
                    print("TOO LONG")

class Lines():
    def __init__(self, trajectories: dict):
        self.trajectories = trajectories

    def fraction_p(self):
        "Compute fraction p of used connections"
        pass
            
    




def load_stations(filepath):
    stations = []
    with open(filepath, 'r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip header
        for row in reader:
            name, y, x = row
            stations.append(Station(name, float(y), float(x)))
    return stations

def load_connections(filepath):
    connections = []
    with open(filepath, 'r') as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            station1, station2, travel_time = row
            connections.append(Connection(station1, station2, int(travel_time)))
            connections.append(Connection(station2, station1, int(travel_time)))
    return connections

if __name__ == "__main__":
    # Inputbestanden
    stations_file = "StationsHolland.csv"
    connections_file = "ConnectiesHolland.csv"

    stations = load_stations(stations_file)

    connections = load_connections(connections_file)
    # print(connections)

    # for c in connections[:5]:
    #         print(c.station1, c.station2)
    # connection_list = [(c.station1, c.station2, c.travel_time) for c in connections]

    train_1 = Trajectory(connections, 55)
    train_1.add_connection('Alkmaar', 'Hoorn')
    print(train_1.traject)
    train_1.add_connection('Hoorn', 'Zaandam')
    print(train_1.traject)

    # create dictionary with each trajectory and its duration
    trajectories = {}
    trajectories['train_1'] = train_1.traject, train_1.duration

    print(trajectories)
    print(len(trajectories))
