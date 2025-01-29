from code.experiment.grid_search import grid_search
from code.visualization.statistics import plot_quality_score_histogram, plot_iteration_scores
import os

# create output directory
output_dir = 'output'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

def run_grid_search(Holland=True, Netherlands=True, run_time=60):
    """ 
    Run the grid search experiment to find the optimal railmap and parameters.

    Input:
        - Holland: Choose to run the experiment for North- and South-Holland
        - Netherlands: Choose to run the experiment for the Netherlands
        - run_time: Maximum time (in seconds) to run each algorithm

    """
    # create kwargs to unpack for paths to csv data
    Holland_kwargs = ("data/StationsHolland.csv",
                    "data/uid_Holland.csv",
                    "data/ConnectiesHolland.csv")
    Netherlands_kwargs = ("data/StationsNationaal.csv", 
                        "data/uid_NL.csv", 
                        "data/ConnectiesNationaal.csv")

    param_grids_Holland = {
    "hillclimber": {
        "iterations": [1000, 5000],
        "num_routes": [4, 5, 6, 7],
        "max_duration": [120]
    },
    "random": {
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
    }}

    param_grids_Netherlands = {
    "hillclimber": {
        "iterations": [1000, 5000],
        "num_routes": [9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20],
        "max_duration": [180]
    },
    "random": {
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
    }}


    # Run grid search for each algorithm
    algorithms = ["random", "random_greedy", "hillclimber", "simulated_annealing"]

    for algorithm in algorithms:
        print(f"\n{'='*50}")
        print(f"Running grid search for {algorithm}")
        print(f"{'='*50}\n")

        if Holland:
            print(f"Holland:\n")
            grid_search(
                *Holland_kwargs,
                algorithm=algorithm,
                param_grids=param_grids_Holland,
                total_time= run_time
            )
        if Netherlands:
            print(f"Netherlands:\n")
            grid_search(
                *Netherlands_kwargs,
                algorithm=algorithm,
                param_grids=param_grids_Netherlands,
                total_time= run_time
            )


def plot_statistics(algorithm="random"):
    """
    Give one of the algorithms to plot the quality scores K per iteration for
    the best railmap both Holland and the Netherlands. Plots are saved to respective folders.
    Choose an algorithm to plot for:
    
    Input:
        - algorithm (str): opt between "random", "random_greedy", "hillclimber", "simulated_annealing"

    Returns:
        - Two plots for both Holland and the Netherlands 
    """
    holland_dir = 'output/Holland'
    national_dir = 'output/Netherlands'
    file_name = f"best_railmap_{algorithm}.json"

    # plot a histogram for the random and greedy algorithms
    if algorithm in ["random", "random_greedy"]:
        plot_quality_score_histogram(os.path.join(holland_dir, file_name), algorithm, 'Holland')
        plot_quality_score_histogram(os.path.join(national_dir, file_name), algorithm, 'Netherlands')

    # plot the course of the iterations for iterative algorithms
    elif algorithm in ["hillclimber", "simulated_annealing"]:
        plot_iteration_scores(os.path.join(holland_dir, file_name), algorithm, 'Holland')
        plot_iteration_scores(os.path.join(national_dir, file_name), algorithm, 'Netherlands')



if __name__ == "__main__":
    """
    Comment a function out with '#' infront of the line of code
    to ensure it does not run.
    """

    ### Run the grid search: ###
    #     Holland: set to False to exclude this region
    #     Netherlands: set to False to exclude this region
    #     run_time: set a maximum time in seconds to let the grid search run per algorithm
    run_grid_search(run_time=1) 
                    # up to 3600 for an hour runtime per algorithm


    ### Plot graphs: ###
        # algorithm: choose between "random", "random_greedy", "hillclimber", "simulated_annealing"
    plot_statistics(algorithm="random_greedy")


    ### Visualize map: ###


    




