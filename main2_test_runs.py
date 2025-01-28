from code.classes.railmap import Railmap
from code.visualization.statistics import plot_hillclimb_sim_ann
from code.algorithms.simulated_annealing import simulated_annealing
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

    output_dir = 'output'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)


    ### Simulated Annealing ###

    output_sim_ann = "output/sim_ann_results.csv"

    # load the railmap
    railmap = Railmap()
    railmap.load_stations(stations_Holland_path, uid_path_Holland, connections_Holland_path)

    # parameters
    iterations = 8000
    max_duration = 120
    num_routes = 7
    init_temp = 3000
    cooling_type = "exponential"
    cooling_rate = 0.999
   
    # run algorithm
    best_railmap, best_score, all_scores, temperatures = simulated_annealing(railmap, iterations, max_duration, num_routes, init_temp, cooling_rate, cooling_type)

    # print results
    print(f"\nBest Quality Score (K): {best_score}")
    for train_name, route in best_railmap.routes.items():
        print(train_name,":",route.route,"\n")

    # write results to CSV
    with open(output_sim_ann, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)

        # write header
        writer.writerow(["iteration", "quality_score", "temperatures"])

        # write all scores and temperatures with iteration index
        for i, (score, temp) in enumerate(zip(all_scores, temperatures), start=1):
            writer.writerow([i, score, temp])


    print(f"Simulated Annealing results have been saved to {output_sim_ann}")

    # plot the graph
    plot_hillclimb_sim_ann(csv_file=output_sim_ann, algorithm='sim_ann')




