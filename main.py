from code..experiment.grid_search import grid_search
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
    Netherlands_kwargs = (stations_NL_path, uid_path_NL, connections_NL_path)

    param_grids_Holland = {
        "hillclimber": {
            "iterations": [1000, 5000],
            "num_routes": [4, 5, 6, 7],
            "max_duration": [120]
        },
        "random_heuristic": {
            "num_routes": [4, 5, 6, 7],
            "iterations": [1000, 5000],
            "max_duration": [120]
        },
        "random_greedy": {
            "num_routes": [4, 5, 6, 7],
            "iterations": [1000, 5000,],
            "max_duration": [120]
        },
        "simulated_annealing": {
            "num_routes": [4, 5, 6, 7],
            "iterations": [1000, 5000],
            "max_duration": [120]
        }
    }

    param_grids_Netherlands = {
        "hillclimber": {
            "iterations": [1000, 5000],
            "num_routes": [9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20],
            "max_duration": [180]
        },
        "random_heuristic": {
            "num_routes": [9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20],
            "iterations": [1000, 5000],
            "max_duration": [180]
        },
        "random_greedy": {
            "num_routes": [9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20],
            "iterations": [1000, 5000],
            "max_duration": [180]
        },
        "simulated_annealing": {
            "num_routes": [9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20],
            "iterations": [1000, 5000],
            "max_duration": [180]
        }
    }


    output_dir = 'output'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)


  # Run grid search for each algorithm
    algorithms = ["hillclimber", "simulated_annealing", "random_heuristic", "random_greedy"]

    for algorithm in algorithms:
        print(f"\n{'='*50}")
        print(f"Running grid search for {algorithm}")
        print(f"{'='*50}\n")

        # Noord- & Zuid Holland
        best_params, best_score, best_routes = grid_search(
            *Holland_kwargs,
            algorithm=algorithm,
            param_grids=param_grids_Holland,
            total_time= 60#3600  # now 15min > finally 1 hour per algorithm
        )

        # Nederland
        best_params, best_score, best_routes = grid_search(
            *Netherlands_kwargs,
            algorithm=algorithm,
            param_grids=param_grids_Netherlands,
            total_time= 60#60  # 1 hour per algorithm
        )
