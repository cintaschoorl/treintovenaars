from code.experiment.grid_search import grid_search
from code.visualization.statistics import plot_quality_score_histogram, plot_iteration_scores
from code.visualization.representation import update
from code.visualization.representation import load_station_short_names
from code.visualization.representation import load_stations
from code.visualization.representation import load_connections
from code.visualization.representation import load_routes


import os
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import json
import networkx as nx
import itertools
import argparse


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
        "iterations": [1000, 5000, 10000],
        "num_routes": [4, 5, 6, 7],
        "max_duration": [120]
    },
    "random": {
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
    }}

    param_grids_Netherlands = {
    "hillclimber": {
        "iterations": [1000, 5000, 10000],
        "num_routes": [9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20],
        "max_duration": [180]
    },
    "random": {
        "num_routes": [9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20],
        "iterations": [1000, 5000, 10000],
        "max_duration": [180]
    },
    "random_greedy": {
        "num_routes": [9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20],
        "iterations": [1000, 5000, 10000],
        "max_duration": [180]
    },
    "simulated_annealing": {
        "num_routes": [9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20],
        "iterations": [1000, 5000, 10000],
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



def visualize_map(algorithm="random"):
    """
    This function initializes the visualization of the best railmap 
    for a chosen algorithm with animation.
    
    Input:
        - algorithm (str): opt between "random", "random_greedy", "hillclimber", "simulated_annealing"
    """
    # Getting the right csv files
    script_dir = os.path.dirname(os.path.abspath(__file__))
    stations_path = "data/StationsNationaal.csv"
    connections_path = "data/ConnectiesNationaal.csv"
    uid_path = "data/uid_NL.csv"
    routes_path = f"output/Netherlands/best_railmap_{algorithm}.json"
    image_path = "data/Nederland_kaart.png"


    # Loading the data
    station_names = load_station_short_names(uid_path)
    stations = load_stations(stations_path)
    connections = load_connections(connections_path)
    routes = load_routes(routes_path)

    # Creating the graph and positions
    G = nx.DiGraph()
    pos = {}
    for station in stations:
        short_name = station_names.get(station.name, station.name)
        G.add_node(short_name)
        pos[short_name] = (station.x, station.y)

    # Adding the connections
    for connection in connections:
        station1_short = station_names.get(connection.station1, connection.station1)
        station2_short = station_names.get(connection.station2, connection.station2)
        G.add_edge(station1_short, station2_short)

    # Assign colors to the routes
    colors = itertools.cycle(["red", "blue", "green", "purple", "orange", "brown", "pink", "cyan"])
    train_colors = {train: next(colors) for train in routes}

    fig, ax = plt.subplots()
    country_map = plt.imread(image_path)

    # Creating the animation
    max_frames = max(len(r) for r in routes.values())
    ani = FuncAnimation(fig, update, fargs=(ax, G, pos, country_map, routes, station_names, train_colors),
                        frames=max_frames, interval=500, repeat=False)

    # Showing the visualization
    plt.tight_layout()
    plt.show()


def parse():
        run_time = int(input("Enter the max runtime for grid search in seconds: "))
        print(f"Running grid search with a max runtime of {run_time} seconds...")
        run_grid_search(run_time=run_time)
        
        while True:
            action = input("Do you want to (plot) statistics or (visualize) the map for the best railmaps? (or type 'exit' to quit): ").strip().lower()
            if action == "exit":
                break
            elif action in ["plot", "visualize"]:
                algorithm = input("Choose an algorithm (random, random_greedy, hillclimber, simulated_annealing): ").strip()
                if action == "plot":
                    print(f"Plotting statistics for {algorithm} algorithm...")
                    plot_statistics(algorithm)
                elif action == "visualize":
                    print(f"Visualizing map for {algorithm} algorithm...")
                    visualize_map(algorithm)
            else:
                print("Invalid choice. Please enter 'plot', 'visualize', or 'exit'.")


if __name__ == "__main__":
    parse()

    