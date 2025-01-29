import time
import csv
import json
from itertools import product
from code.classes.railmap import Railmap
from code.algorithms.hillclimber import hill_climber
from code.algorithms.simulated_annealing import simulated_annealing
from code.algorithms.randomise import randomise_heuristics
from code.algorithms.random_greedy import random_greedy_algorithm
from code.classes.route import Route


param_grids_Holland = {
    "hillclimber": {
        "iterations": [1000, 5000, 10000],
        "num_routes": [4, 5, 6, 7],
        "max_duration": [120]
    },
    "random_heuristic": {
        "num_routes": [4, 5, 6, 7],
        "iterations": [1000, 5000, 10000],
        "max_duration": [120]
    },
    "random_greedy": {
        "num_routes": [4, 5, 6, 7],
        "iterations": [1000, 5000, 10000],
        "max_duration": [120]
    },
    "simulated_annealing": {
        "num_routes": [4, 5, 6, 7],
        "iterations": [1000, 5000, 10000],
        "max_duration": [120]
    }
}


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


def grid_search(stations_path, uid_path, connections_path, algorithm="hillclimber", param_grids=param_grids_Holland, total_time=3600):
    """
    Perform grid search for parameter tuning with exact timing control.
    Save the best railmap and parameters in a CSV file.
    """
    start_time = time.time()

    # param_grids = {
    #     "hillclimber": {
    #         "iterations": [1000, 5000, 10000],
    #         "num_routes": [4, 5, 6, 7],
    #         "max_duration": [120]
    #     },
    #     "random_heuristic": {
    #         "num_routes": [4, 5, 6, 7],
    #         "iterations": [1000, 5000, 10000],
    #         "max_duration": [120]
    #     },
    #     "random_greedy": {
    #         "num_routes": [4, 5, 6, 7],
    #         "iterations": [1000, 5000, 10000],
    #         "max_duration": [120]
    #     },
    #     "simulated_annealing": {
    #         "num_routes": [4, 5, 6, 7],
    #         "iterations": [1000, 5000, 10000],
    #         "max_duration": [120]
    #     }
    # }

    grid = param_grids[algorithm]
    param_names = sorted(grid.keys())
    param_values = [grid[name] for name in param_names]
    combinations = list(product(*param_values))

    results_file = f"output/grid_search_{algorithm}.csv"
    with open(results_file, 'w', newline='') as f:
        writer = csv.writer(f)
        header = param_names + ['score', 'n_runs', 'best_routes']
        writer.writerow(header)

    best_params = None
    best_score = 0
    best_railmap = None
    best_all_scores = []  # To store all scores for plotting the course of K


    for combo in combinations:
        params = dict(zip(param_names, combo))
        print(f"\nTesting parameters: {params}")

        combo_scores = []
        n_runs = 0

        combo_start_time = time.time()
        remaining_time = total_time - (combo_start_time - start_time)
        time_per_combo = remaining_time / len(combinations)

        while time.time() - combo_start_time < time_per_combo:
            railmap = Railmap()
            railmap.load_stations(stations_path, uid_path, connections_path)

            score, railmap_result, all_scores = run_algorithm_with_timeout(
                algorithm,
                railmap,
                params,
                stations_path,
                uid_path,
                connections_path
            )

            combo_scores.append(score)
            n_runs += 1

            # Track all iteration scores for plotting the course of K
            if all_scores:
                best_all_scores.append({
                    'params': params,
                    'iteration_scores': all_scores
                })

            if score > best_score:
                best_score = score
                best_params = params
                best_railmap = railmap_result
                best_all_scores = all_scores  # Store all scores related to this best railmap
                print(f"New best score: {best_score}")


        avg_score = sum(combo_scores) / len(combo_scores) if combo_scores else 0

        # Serialize routes into a string for saving
        best_route_str = ""
        if best_railmap:
            route_list = []
            for train_id, route in best_railmap.routes.items():
                station_names = [station.name for station in route.route]
                route_list.append(f"{train_id}: {' -> '.join(station_names)}")
            best_route_str = " | ".join(route_list)

        with open(results_file, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([*combo, avg_score, n_runs, best_route_str])

        if time.time() - start_time >= total_time:
            print(f"Time limit of {total_time} seconds reached")
            break

    total_runtime = time.time() - start_time
    print(f"\nTotal runtime: {total_runtime:.0f} seconds")

    # Save the best railmap to a JSON file
    if best_railmap:
        with open(f"output/best_railmap_{algorithm}.json", 'w') as f:
            json.dump({
                "parameters": best_params,
                "score": best_score,
                "routes": {
                    train_id: [station.name for station in route.route]
                    for train_id, route in best_railmap.routes.items()
                },
                "iteration_scores": best_all_scores  # Save all scores for this best railmap
            }, f, indent=4)


    #  # Save the iteration-wise scores for Hill Climber and Simulated Annealing to JSON
    # if algorithm in ["hillclimber", "simulated_annealing"] and best_all_scores:
    #     with open(f"output/iteration_scores_{algorithm}.json", 'w') as f:
    #         json.dump(best_all_scores, f, indent=4)

    # Print final best results
    print(f"\nBest score: {best_score}")
    print(f"Best parameters: {best_params}")
    print("\nBest routes:")
    for train_id, route in best_railmap.routes.items():
        print(f"{train_id}: {[station.name for station in route.route]}")

    return best_params, best_score, best_railmap
