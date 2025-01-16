from code.classes.railmap import Railmap
from code.algorithms import randomise



if __name__ == "__main__":
    # create paths to csv data
    stations_path = "data/StationsHolland.csv"
    connections_path = "data/ConnectiesHolland.csv"
    uid_path = "data/uid.csv"

    railsystem = Railmap()

    # load the csv files to get all stations and connections
    railsystem.load_stations(stations_path, uid_path, connections_path)

    # create random route
    route1, r1_time = randomise.randomise_route(railsystem.stations, 120)
    print(f"\nRandom route: {route1}\nTotal duration: {r1_time}")

    K_route1 = railsystem.quality_K(route1, r1_time)
    print(f"Quality of route 1: {K_route1}")
