import random
from code.classes.route import Route
from code.classes.railmap import Railmap



if __name__ == "__main__":
    # create paths to csv data
    stations_path = "data/StationsHolland.csv"
    connections_path = "data/ConnectiesHolland.csv"
    uid_path = "data/uid.csv"

    railsystem = Railmap()

    # load the csv files to get all stations and connections
    railsystem.load_stations(stations_path, uid_path, connections_path)
    print(railsystem.stations)

    # test run to print the attributes of a random station
    random_station = random.choice(railsystem.stations)
    print(f"Name: {random_station.name}\nCoordinates: {random_station.coordinates}\nNeighbours: {random_station.neighbours}")
