import time
import csv
from itertools import product
from code.classes.railmap import Railmap
from code.algorithms.hillclimber import hill_climber
from code.algorithms.simulated_annealing import simulated_annealing
from code.algorithms.randomise import randomise_heuristics
from code.algorithms.random_greedy import random_greedy_algorithm
from code.classes.route import Route

def run_algorithm_with_timeout(algorithm_name, railmap, params, stations_path, uid_path, connections_path):
    """
    Run an algorithm and return the best score
    """
    try:
        if algorithm_name == "hillclimber":
            best_railmap, best_score, _ = hill_climber(railmap, **params)
            return best_score, best_railmap.routes

        elif algorithm_name == "simulated_annealing":
            best_railmap, best_score, _, _= simulated_annealing(railmap, **params)
            return best_score, best_railmap.routes

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
            return railmap.quality_K(), railmap.routes

        else:
            temp_output = f"output/temp_random_greedy.csv"

            best_score, routes = random_greedy_algorithm(
                stations_path,
                uid_path,
                connections_path,
                params['num_routes'],
                params['max_duration'],
                params['iterations'],
                temp_output
            )
        return best_score, routes

    except Exception as e:
        print(f"Error running algorithm: {e}")
        return 0

def grid_search(stations_path, uid_path, connections_path, algorithm="hillclimber", total_time=3600):
    """
    Perform grid search for parameter tuning with exact timing control
    """
    start_time = time.time()

    param_grids = {
        "hillclimber": {
            "iterations": [1000, 10000],
            "num_routes": [4, 5, 6, 7],
            "max_duration": [120]
        },
        "random_heuristic": {
            "num_routes": [4, 5, 6, 7],
            "iterations": [1000, 10000],
            "max_duration": [120]
        },
        "random_greedy": {
            "num_routes": [4, 5, 6, 7],
            "iterations": [1000, 10000],
            "max_duration": [120]
        },
        "simulated_annealing": {
            "num_routes": [4, 5, 6, 7],
            "iterations": [1000, 10000],
            "max_duration": [120]
        }

    }

    grid = param_grids[algorithm]
    param_names = sorted(grid.keys())
    param_values = [grid[name] for name in param_names]
    combinations = list(product(*param_values))

    results_file = f"output/grid_search_{algorithm}.csv"
    with open(results_file, 'w', newline='') as f:
        writer = csv.writer(f)
        header = param_names + ['score', 'n_runs', 'best_route']
        writer.writerow(header)

    best_params = None
    best_score = 0
    best_routes = None

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

            score, routes = run_algorithm_with_timeout(
                algorithm,
                railmap,
                params,
                stations_path,
                uid_path,
                connections_path
            )

            combo_scores.append(score)
            n_runs += 1

            if score > best_score:
                best_score = score
                best_params = params
                best_routes = routes
                print(f"New best score: {best_score}")

        avg_score = sum(combo_scores) / len(combo_scores) if combo_scores else 0

        best_route_str = ""
        if best_routes:
            route_list = []
            for train_id, route in best_routes.items():
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

    # Print final best results
    print(f"\nBest score: {best_score}")
    print(f"Best parameters: {best_params}")
    print("\nBest routes:")
    for train_id, route in best_routes.items():
        print(f"{train_id}: {[station.name for station in route.route]}")

    return best_params, best_score, best_routes
