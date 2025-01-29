import time
import json
import os
from itertools import product
from code.classes.railmap import Railmap
from code.algorithms.hillclimber import hill_climber
from code.algorithms.simulated_annealing import simulated_annealing
from code.algorithms.randomise import run_randomise_heuristics
from code.algorithms.random_greedy import random_greedy_algorithm
from code.classes.route import Route


def run_algorithm_with_timeout(algorithm_name, railmap, params, stations_path, uid_path, connections_path):
    """
    Run an algorithm and return the best score and best railmap.

    Input:
        - algorithm_name (str): Name of the algorithm to run
        - railmap (Railmap): The initial railmap object to be modified by the algorithm
        - params (dict): Parameters to be passed to the algorithm
        - stations_path (str): Path to the stations CSV file
        - uid_path (str): Path to the UID CSV file
        - connections_path (str): Path to the connections CSV file

    Returns:
        - best_score (float): The best score achieved by the algorithm
        - best_railmap (Railmap): The railmap with the best routes found
        - all_scores (list): List of all scores during the algorithm's execution
    """
    try:
        # run the algorithm based on the algorithm_name
        if algorithm_name == "hillclimber":
            best_railmap, best_score, all_scores = hill_climber(railmap, **params)
            return best_score, best_railmap, all_scores

        elif algorithm_name == "simulated_annealing":
            best_railmap, best_score, all_scores, _ = simulated_annealing(railmap, **params)
            return best_score, best_railmap, all_scores

        elif algorithm_name == "random_heuristic":
            best_score, best_railmap, all_scores = run_randomise_heuristics(stations_path, uid_path, connections_path, **params)
            return best_score, best_railmap, all_scores

        else: =
            temp_output = f"output/temp_random_greedy.csv"
            best_score, routes, all_scores = random_greedy_algorithm(
                stations_path,
                uid_path,
                connections_path,
                params['num_routes'],
                params['max_duration'],
                params['iterations'],
                temp_output
            )
            railmap.routes = routes
            return best_score, railmap, all_scores

    except Exception as e:
        print(f"Error running algorithm: {e}")
        return 0, None, []


def grid_search(stations_path, uid_path, connections_path, algorithm, param_grids, total_time=3600, output_dir='output'):
    """
    Perform grid search for parameter tuning with a time limit.
    Saves one JSON file per region and algorithm combination.

    Input:
        - stations_path (str): Path to the stations CSV file
        - uid_path (str): Path to the UID CSV file
        - connections_path (str): Path to the connections CSV file
        - algorithm (str): The algorithm name to use
        - param_grids (dict): A dictionary containing possible parameter values for the grid search
        - total_time (int): The time limit for the grid search in seconds (default is 3600 seconds)
        - output_dir (str): The directory where the output JSON files will be saved (default is 'output')

    Returns:
        - None, the best results are saved in the output directory
    """
    start_time = time.time()

    # Prepare the parameter grid
    grid = param_grids[algorithm]
    param_combinations = list(product(*[grid[key] for key in sorted(grid.keys())]))

    best_params, best_score, best_railmap, best_iteration_scores = None, 0, None, []

    # Determine the region based on the stations_path
    if 'Holland' in stations_path:
        region = 'Holland'
    else:
        region = 'Netherlands'

    # Create the region folder
    region_output_dir = os.path.join(output_dir, region)
    if not os.path.exists(region_output_dir):
        os.makedirs(region_output_dir)

    # Start testing different parameter combinations
    for combo in param_combinations:
        params = dict(zip(sorted(grid.keys()), combo))
        print(f"Testing parameters: {params}")

        # Initialize railmap and load stations
        railmap = Railmap()
        railmap.load_stations(stations_path, uid_path, connections_path)

        # Run the algorithm with the current parameters
        score, railmap_result, iteration_scores = run_algorithm_with_timeout(
            algorithm, railmap, params, stations_path, uid_path, connections_path
        )

        # Update the best results if the current score is better
        if score > best_score:
            best_score, best_params, best_railmap, best_iteration_scores = score, params, railmap_result, iteration_scores
            print(f"New best score: {best_score}")

        # Stop if the total time limit is reached
        if time.time() - start_time >= total_time:
            print(f"Time limit of {total_time} seconds reached")
            break

    # Save the best results in a JSON file for each algorithm
    if best_railmap:
        json_output_path = os.path.join(region_output_dir, f"best_railmap_{algorithm}.json")
        with open(json_output_path, 'w') as f:
            json.dump({
                "parameters": best_params,
                "score": best_score,
                "routes": {train_id: [station.name for station in route.route] for train_id, route in best_railmap.routes.items()},
                "iteration_scores": best_iteration_scores
            }, f, indent=4)

        print(f"Best results saved to {json_output_path}\n")
