from code.algorithms.grid_search import grid_search
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
            total_time= 900  # now 15min > finally 1 hour per algorithm
        )

        # # Nederland
        # best_params, best_score, best_routes = grid_search(
        #     *Netherlands_kwargs,
        #     algorithm=algorithm,
        #     total_time=60  # 1 hour per algorithm
        # )
