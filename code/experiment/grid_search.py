import time
import json
import os
from itertools import product
from code.classes.railmap import Railmap
from code.algorithms.hillclimber import hill_climber
from code.algorithms.simulated_annealing import simulated_annealing
from code.algorithms.randomise import randomise_heuristics
from code.algorithms.random_greedy import random_greedy_algorithm
from code.classes.route import Route


def run_algorithm_with_timeout(algorithm_name, railmap, params, stations_path, uid_path, connections_path):
    """
    Run an algorithm and return the best score and best railmap (if applicable).
    """
    try:
        if algorithm_name == "hillclimber":
            best_railmap, best_score, all_scores = hill_climber(railmap, **params)
            return best_score, best_railmap, all_scores

        elif algorithm_name == "simulated_annealing":
            best_railmap, best_score, all_scores, _ = simulated_annealing(railmap, **params)
            return best_score, best_railmap, all_scores

        elif algorithm_name == "random_heuristic":
            for i in range(params['num_routes']):
                first_route = (i == 0)
                route_stations, total_time = randomise_heuristics(
                    railmap.stations,
                    params['max_duration'],
                    first_route
                )
                route = Route(railmap.stations, params['max_duration'])
                route.route = route_stations
                route.travel_time = total_time
                route.id = f"train_{i + 1}"
                railmap.add_trajectory(route)
            return railmap.quality_K(), railmap, all_scores

        else:  # random_greedy
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
            railmap.routes = routes  # Save routes back to railmap
            return best_score, railmap, all_scores

    except Exception as e:
        print(f"Error running algorithm: {e}")
        return 0, None, []


def grid_search(stations_path, uid_path, connections_path, algorithm, param_grids, total_time=3600, output_dir='output'):
    """
    Perform grid search for parameter tuning with a time limit.
    Saves one JSON file per region and algorithm combination.
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

    # Start testing parameter combinations
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
