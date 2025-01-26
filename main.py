from code.classes.railmap import Railmap
from code.algorithms.randomise import randomise_route
from code.algorithms.randomise import randomise_heuristics
from code.algorithms.random_greedy import random_greedy_algorithm
from code.algorithms.hillclimber import hill_climber
from  code.classes.route import Route
from code.visualization.statistics import plot_hill_climber
from code.visualization.statistics import plot_random
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

    # ### Random ###

    # output_random = "output/random_results.csv"

    # # Create CSV header
    # with open(output_random, 'w', newline='') as csvfile:
    #     writer = csv.writer(csvfile)
    #     writer.writerow(['quality_score'])

    # # het random algoritme 10000 keer laten runnen
    # for iteration in range(10000):
    #     railsystem = Railmap()

    #     # load the csv files to get all stations and connections
    #     railsystem.load_stations(stations_path, uid_path, connections_path)

    #     number_routes = 7
    #     max_duration = 120

    #     for i in range(number_routes):
    #         route_stations, total_time = randomise_route(railsystem.stations, max_duration)

    #         route = Route(railsystem.stations, max_duration)
    #         route.route = route_stations
    #         #print(route.route)
    #         route.travel_time = total_time
    #         route.id = f"train_{i + 1}"

    #         railsystem.add_trajectory(route)

    #     K = railsystem.quality_K()
    #         #print(f"\n quality score: {K}")

    #         # Write result to CSV
    #     with open(output_random, 'a', newline='') as csvfile:
    #         writer = csv.writer(csvfile)
    #         writer.writerow([K])

    # print(f"\nRandom results have been saved to {output_random}")


    # output_random_heur = "output/random_heur_results.csv"

    # # Create CSV header
    # with open(output_random_heur, 'w', newline='') as csvfile:
    #         writer = csv.writer(csvfile)
    #         writer.writerow(['quality_score'])

    # # het random algoritme met heuristieken 10000 keer laten runnen
    # for iteration in range(10000):
    #     railsystem = Railmap()

    #     # load the csv files to get all stations and connections
    #     railsystem.load_stations(stations_path, uid_path, connections_path)

    #     number_routes = 7
    #     max_duration = 120

    #     for i in range(number_routes):
    #          # geef aan dat dit de eerste route is van een nieuwe lijnvoering
    #         first_route = (i == 0)

    #         route_stations, total_time = randomise_heuristics(
    #             railsystem.stations,
    #             max_duration,
    #             first_route
    #         )

    #         route = Route(railsystem.stations, max_duration)
    #         route.route = route_stations
    #         #print(route.route)
    #         route.travel_time = total_time
    #         route.id = f"train_{i + 1}"

    #         railsystem.add_trajectory(route)

    #     K = railsystem.quality_K()
    #         #print(f"\n quality score: {K}")

    #             # Write result to CSV
    #     with open(output_random_heur, 'a', newline='') as csvfile:
    #         writer = csv.writer(csvfile)
    #         writer.writerow([K])

    # print(f"\nRandom with heuristics results have been saved to {output_random_heur}")

    # # make a histogram of the K values in csv file
    # plot_random('output/random_results.csv')
    # plot_random('output/random_heur_results.csv')



    ### Random Greedy ###

    # creating an output csv file
    output_random_greedy = "output/random_greedy_results.csv"

    with open(output_random_greedy, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['quality_score'])


    # initializing some values
    iterations_rg = 1000
    num_routes_rg = 7
    max_duration_rg = 120

    # calling the random greedy algorithm for each iteration
    for iteration in range(iterations_rg):

        railsystem_rg = Railmap()
        railsystem_rg.load_stations(stations_path, uid_path, connections_path)

        quality_score = random_greedy_algorithm(stations_path, uid_path, connections_path, num_routes_rg, max_duration_rg, iterations_rg)

        with open(output_random_greedy, 'a', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([quality_score])

    print(f"\nRandom Greedy results have been saved to {output_random_greedy}")




    ### Hill Climber ###

    output_hillclimber = "output/hillclimber_results.csv"

    # load the railmap
    railmap = Railmap()
    railmap.load_stations(stations_path, uid_path, connections_path)

    # parameters
    iterations = 1000
    num_routes = 4
    max_duration = 120

    # run algorithm
    best_railmap, best_score, all_scores = hill_climber(railmap, iterations, max_duration, num_routes)

    # print results
    print(f"\nBest Quality Score (K): {best_score}")
    for train_name, route in best_railmap.routes.items():
        print(train_name,":",route.route,"\n")

    # write results to CSV
    with open(output_hillclimber, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)

        # write header
        writer.writerow(["iteration", "quality_score"])

        # write all scores with iteration index
        for i, score in enumerate(all_scores, start=1):
            writer.writerow([i, score])

    print(f"Hill Climber results have been saved to {output_hillclimber}")

    plot_hill_climber()
