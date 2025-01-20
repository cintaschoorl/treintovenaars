from code.classes.railmap import Railmap
from code.algorithms.randomise import randomise_route
from  code.classes.route import Route



if __name__ == "__main__":
    # create paths to csv data
    stations_path = "data/StationsHolland.csv"
    connections_path = "data/ConnectiesHolland.csv"
    uid_path = "data/uid.csv"

    railsystem = Railmap()

    # load the csv files to get all stations and connections
    railsystem.load_stations(stations_path, uid_path, connections_path)

    number_routes = 7
    max_duration = 120

    for i in range(number_routes):
        route_stations, total_time = randomise_route(railsystem.stations, max_duration)

        route = Route(railsystem.stations, max_duration)
        route.route = route_stations
        route.id = f"train_{i + 1}"

        railsystem.add_trajectory(route)

    K = railsystem.quality_K()
    print(f"\nTotal quality score: {K}")

    # create random route
    #route1, r1_time = randomise.randomise_route(railsystem.stations, 120)
    #print(f"\nRandom route: {route1}\nTotal duration: {r1_time}")

    #K_route1 = railsystem.quality_K(route1, r1_time)
    #print(f"Quality of route 1: {K_route1}")
