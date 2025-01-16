import csv
from code.classes.route import Route
from code.classes.railmap import Railmap
from code.classes.connection import Connection



if __name__ == "__main__":
    # create paths to csv data
    stations_path = "data/StationsHolland.csv"
    connections_path = "data/ConnectiesHolland.csv"
    uid_path = "data/uid.csv"

    railsystem = Railmap()

    # load the csv files to get all stations and connections
    railsystem.load_stations(stations_path, uid_path, connections_path)
    print(railsystem.stations)


    station1 = railsystem.stations["Amsterdam Centraal"]
    station2 = railsystem.stations["Amsterdam Sloterdijk"]
    connection1 = Connection(station1, station2, 15)

    station3 = railsystem.stations["Utrecht Centraal"]
    station4 = railsystem.stations["Amersfoort"]
    connection2 = Connection(station3, station4, 20)

    train_connections = [connection1, connection2]

    train = ('train001', train_connections)

    railsystem.add_trajectory(train)

    #railsystem.add_trajectory(railsystem.trajectories)
    print(railsystem.trajectories)

    # print(type(Railmap.quality_K))
    # print(Railmap.quality_K)
