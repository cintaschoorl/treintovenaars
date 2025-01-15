import csv
from code.classes.route import Route
from code.classes.railmap import Railmap



if __name__ == "__main__":
    # create paths to csv data
    stations_path = "data/StationsHolland.csv"
    connections_path = "data/ConnectiesHolland.csv"
    uid_path = "data/uid.csv"

    # create a rail system
    railsystem = Railmap()

    # load the csv files to get all stations and connections
    railsystem.load_all_files(stations_path, uid_path, connections_path)
    print(railsystem.stations)
