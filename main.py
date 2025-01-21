from code.classes.railmap import Railmap
from code.algorithms.randomise import randomise_route
from  code.classes.route import Route
import csv
import os


if __name__ == "__main__":
    # create paths to csv data
    stations_path = "data/StationsHolland.csv"
    connections_path = "data/ConnectiesHolland.csv"
    uid_path = "data/uid.csv"

    output_dir = 'output'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    output_file = "output/random_results.csv"

    # Create CSV header
    with open(output_file, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['quality_score'])

    # het algoritme 500 keer laten runnen
    for iteration in range(500):
        railsystem = Railmap()

        # load the csv files to get all stations and connections
        railsystem.load_stations(stations_path, uid_path, connections_path)

        number_routes = 7
        max_duration = 120

        for i in range(number_routes):
            route_stations, total_time = randomise_route(railsystem.stations, max_duration)

            route = Route(railsystem.stations, max_duration)
            route.route = route_stations
            #print(route.route)
            route.travel_time = total_time
            route.id = f"train_{i + 1}"

            railsystem.add_trajectory(route)

        K = railsystem.quality_K()
            #print(f"\n quality score: {K}")

            # Write result to CSV
        with open(output_file, 'a', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([K])

    print(f"\nResults have been saved to {output_file}")

    # create random route
    #route1, r1_time = randomise.randomise_route(railsystem.stations, 120)
    #print(f"\nRandom route: {route1}\nTotal duration: {r1_time}")

    #K_route1 = railsystem.quality_K(route1, r1_time)
    #print(f"Quality of route 1: {K_route1}")
