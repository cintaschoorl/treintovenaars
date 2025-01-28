from code.classes.railmap import Railmap
from code.algorithms.randomise import randomise_route
from code.algorithms.randomise import run_randomise_route
from code.algorithms.randomise import randomise_heuristics
from code.algorithms.randomise import run_randomise_heuristics
from code.algorithms.random_greedy import random_greedy_algorithm
from code.algorithms.hillclimber import hill_climber
from code.classes.route import Route
from code.visualization.statistics import plot_hillclimb_sim_ann
from code.visualization.statistics import plot_random
from code.visualization.statistics import plot_random_greedy
from code.algorithms.grid_search import grid_search
import csv
import os

if __name__ == "__main__":
    # create paths to csv data
    stations_Holland_path = "data/StationsHolland.csv"
    stations_NL_path = "data/StationsNationaal.csv"
    connections_Holland_path = "data/ConnectiesHolland.csv"
    connections_NL_path = "data/ConnectiesNationaal.csv"
    uid_path_Holland = "data/uid_Holland.csv"
    uid_path_NL = "data/uid_NL.csv"

    Holland_kwargs = (stations_Holland_path, uid_path_Holland, connections_Holland_path)
    NL_kwargs = (stations_NL_path, uid_path_NL, connections_NL_path)


    output_dir = 'output'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)


    #
    # # ### Random algorithms ###
    #
    # # Run random algorithm Holland
    # output_random = "output/random_results_Holland.csv"
    # run_randomise_route(stations_Holland_path, uid_path_Holland, connections_Holland_path, output_random)
    #
    # # Run random algorithm on NL
    # output_random_NL = "output/random_results_NL.csv"
    # run_randomise_route(stations_NL_path, uid_path_NL, connections_NL_path, output_random_NL, num_routes=20, max_duration=180)
    #
    # # Run random heuristic algorithm
    # output_random_heur = "output/random_heur_results_Holland.csv"
    # run_randomise_heuristics(stations_Holland_path, uid_path_Holland, connections_Holland_path, output_random_heur)
    #
    # # Run random heuristic algorithm
    # output_random_heur_NL = "output/random_heur_results_NL.csv"
    # run_randomise_heuristics(stations_NL_path, uid_path_NL, connections_NL_path, output_random_heur_NL, num_routes=20, max_duration=180)
    #
    # # make a histogram of the K values in csv file
    # plot_random(output_random)
    # plot_random(output_random_NL)
    # plot_random(output_random_heur)
    # plot_random(output_random_heur_NL)
    #

    ### Random Greedy ###

    # initializing some values
    iterations_rg_Holland = 10000
    num_routes_rg_Holland = 7
    max_duration_rg_Holland = 120

    iterations_rg_NL = 10000
    num_routes_rg_NL = 20
    max_duration_rg_NL = 180


    output_random_greedy_Holland = "output/random_greedy_Holland_results.csv"
    output_random_greedy_NL = "output/random_greedy_NL_results.csv"


    with open(output_random_greedy_Holland, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['iteration', 'quality_score'])

    with open(output_random_greedy_NL, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['iteration', 'quality_score'])



    # running the algorithm and writing results in a csv file for each iteration
    quality_score_Holland, routes_Holland = random_greedy_algorithm(*Holland_kwargs, num_routes_rg_Holland, max_duration_rg_Holland, iterations_rg_Holland, output_random_greedy_Holland)
    quality_score_NL, routes_NL= random_greedy_algorithm(*NL_kwargs, num_routes_rg_NL, max_duration_rg_NL, iterations_rg_NL, output_random_greedy_NL)
    print(routes_Holland)

    print(f"\nRandom Greedy results have been saved to {output_random_greedy_Holland}")
    print(f"\nRandom Greedy results have been saved to {output_random_greedy_NL}")


    plot_random_greedy(output_random_greedy_Holland)
    plot_random_greedy(output_random_greedy_NL)



    # ### Hill Climber ###
    #
    # output_hillclimber = "output/hillclimber_results.csv"
    #
    # # load the railmap
    # railmap = Railmap()
    # railmap.load_stations(stations_NL_path, uid_path_NL, connections_NL_path)
    #
    # # parameters
    # iterations = 50
    # num_routes = 4
    # max_duration = 120
    #
    # # run algorithm
    # best_railmap, best_score, all_scores = hill_climber(railmap, iterations, max_duration, num_routes)
    #
    # # print results
    # print(f"\nBest Quality Score (K): {best_score}")
    # for train_name, route in best_railmap.routes.items():
    #     print(train_name,":",route.route,"\n")
    #
    # # write results to CSV
    # with open(output_hillclimber, 'w', newline='') as csvfile:
    #     writer = csv.writer(csvfile)
    #
    #     # write header
    #     writer.writerow(["iteration", "quality_score"])
    #
    #     # write all scores with iteration index
    #     for i, score in enumerate(all_scores, start=1):
    #         writer.writerow([i, score])
    #
    # print(f"Hill Climber results have been saved to {output_hillclimber}")
    #
    # plot_hill_climber()




  #
  # # Run grid search for each algorithm
  #   algorithms = ["hillclimber", "simulated_annealing", "random_heuristic", "random_greedy"]
  #
  #   for algorithm in algorithms:
  #       print(f"\n{'='*50}")
  #       print(f"Running grid search for {algorithm}")
  #       print(f"{'='*50}\n")
  #
  #       best_params, best_score, best_routes = grid_search(
  #           stations_Holland_path,
  #           uid_path_Holland,
  #           connections_Holland_path,
  #           algorithm=algorithm,
  #           total_time=100  # 1 hour per algorithm
  #       )
