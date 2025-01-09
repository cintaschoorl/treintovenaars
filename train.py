import csv

class Station:
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

class Connection:
    """
    Represents a connection between two train stations with a travel time.
    Attributes are: names and travel time.
    """
    def __init__(self, station1, station2, travel_time):
        self.station1 = station1
        self.station2 = station2
        self.travel_time = travel_time

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
    connection_list = [(c.station1, c.station2, c.travel_time) for c in connections]

    print(station_list)
    print(connection_list)
