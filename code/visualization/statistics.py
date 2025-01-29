import json
import matplotlib.pyplot as plt
import os

def plot_quality_score_histogram(json_file: json, algorithm: str, region: str):
    """
    Plots a histogram of quality scores for Random and Random Greedy algorithms.
    
    Input:
        - json_file (json): path to the JSON file containing quality scores
        - algorithm (str): name of the algorithm (for title and file naming)
    """
    # load JSON data
    with open(json_file, 'r') as file:
        data = json.load(file)
    
    # extract quality scores
    quality_scores = data.get("iteration_scores", [])
    
    if not quality_scores:
        print("No quality scores found in the JSON file.")
        return
    
    # create histogram
    plt.figure(figsize=(10, 6))
    plt.hist(quality_scores, bins=20, edgecolor='black', alpha=0.75)
    
    plt.title(f"Distribution of Quality Scores for {algorithm.capitalize()} Algorithm")
    plt.xlabel("Quality Score (K)")
    plt.ylabel("Frequency")
    plt.grid(True)
    
    # save to correct output path
    output_dir = f'output/{region}'
    os.makedirs(output_dir, exist_ok=True)

    # save the plot
    output_path = os.path.join(output_dir, f"{algorithm}_quality_score_histogram.png")
    plt.savefig(output_path)
    print(f"Plot saved to {output_path}")
    
    # show plot
    plt.show()

def plot_iteration_scores(json_file: json, algorithm: str, region: str):
    """
    Plots the iteration scores over iterations for Hill Climber and Simulated Annealing algorithms.
    
    Input:
        - json_file (json): path to the JSON file containing iteration scores.
        - algorithm (str): name of the algorithm (for title and file naming).
    """
    # load JSON data
    with open(json_file, 'r') as file:
        data = json.load(file)
    
    # extract iteration scores
    iteration_scores = data.get("iteration_scores", [])
    
    if not iteration_scores:
        print("No iteration scores found in the JSON file.")
        return
    
    # generate x-axis (iteration numbers)
    iterations = list(range(1, len(iteration_scores) + 1))
    
    # create plot
    plt.figure(figsize=(10, 6))
    plt.plot(iterations, iteration_scores, marker='o', linestyle='-', color='blue', label='Quality Score (K)')
    
    plt.title(f"{algorithm.capitalize()}: Optimization of Quality Score (K)")
    plt.xlabel("Iterations")
    plt.ylabel("Quality Score (K)")
    plt.grid(True)
    plt.legend()

    # save to correct output path
    output_dir = f'output/{region}'
    os.makedirs(output_dir, exist_ok=True)

    # save the plot
    output_path = os.path.join(output_dir, f"{algorithm}_iteration_scores.png")
    plt.savefig(output_path)
    print(f"Plot saved to {output_path}")
        
    # show plot
    plt.show()

if __name__ == "__main__":
    plot_quality_score_histogram("output/best_railmap_random.json", "random")
    plot_quality_score_histogram("output/best_railmap_greedy.json", "greedy")
    plot_iteration_scores("output/best_railmap_hillclimber.json", "hillclimber")
    plot_iteration_scores("output/best_railmap_sim_ann.json", "sim_ann")


# # Visualize Random
# def plot_random(input_file):
#     output_path = '../../output/quality_scores_histogram.png'
#     # Lees de CSV file
#     df = pd.read_csv(input_file)

#     # Maak het histogram
#     plt.figure(figsize=(10, 6))
#     plt.hist(df['quality_score'], bins=20, edgecolor='black')
#     plt.title('Distribution of Quality Scores (K) for Random Algorithm')
#     plt.xlabel('Quality Score (K)')
#     plt.ylabel('Frequency')

#     # Voeg gemiddelde en standaarddeviatie toe aan de plot
#     mean = df['quality_score'].mean()
#     std = df['quality_score'].std()
#     plt.axvline(mean, color='red', linestyle='dashed', linewidth=1)
#     plt.text(mean*1.1, plt.ylim()[1]*0.9, f'Mean: {mean:.2f}\nStd: {std:.2f}')

#     # Sla de plot op
#     plt.savefig('output/quality_scores_histogram.png')
#     plt.show()


# # visualize random greedy
# def plot_random_greedy(input_file):
#     """
#     Visualizing the distribution of quality scores from the random greedy algorithm.
#     """
#     df = pd.read_csv(input_file)

#     # Creating the histogram
#     plt.figure(figsize=(10, 6))
#     plt.hist(df['quality_score'], bins=20, edgecolor='black', alpha=0.75)
#     plt.title('Distribution of Quality Scores for Random Greedy Algorithm')
#     plt.xlabel('Quality Score (K)')
#     plt.ylabel('Frequency')

#     # Adding the mean and the standard deviation values to the plot
#     mean = df['quality_score'].mean()
#     std = df['quality_score'].std()
#     plt.axvline(mean, color='red', linestyle='dashed', linewidth=1)
#     plt.text(mean * 1.05, plt.ylim()[1] * 0.9, f'Mean: {mean:.2f}\nStd: {std:.2f}', color='black')

#     # Plotting
#     file_name = os.path.basename(input_file).replace(".csv", "")
#     plt.savefig(f'output/quality_scores_histogram_{file_name}.png')
#     plt.show()

# # Visualize Hill Climber or Simulated Annealing
# def plot_hillclimb_sim_ann(csv_file="output/hillclimber_results.csv", algorithm='hillclimber'):
#     """
#     Plots the course of the quality function K to the iterations.

#     Input:
#         - csv_file (.csv): iterations in the first row and K in the second
#         - algorithm (str): choose which algorithm to plot: 'hillclimber' / 'sim_ann'

#     """
#     iterations = []
#     scores = []
#     temperatures = []

#     # read CSV file
#     with open(csv_file, 'r') as file:
#         reader = csv.reader(file)
#         next(reader)  # skip header

#         for row in reader:
#             iterations.append(int(row[0]))
#             scores.append(int(row[1]))
#             if algorithm == "sim_ann":
#                 temperatures.append(float(row[2]))

#      # create plot
#     plt.figure(figsize=(10, 6))
#     plt.plot(iterations, scores, label="Quality Score (K)", color='blue', marker='o')  # Quality scores

#     if algorithm == 'sim_ann':
#         plt.title("Simulated Annealing: optimization of quality score K")
#         # plot temperatures as a red line
#         plt.plot(iterations, temperatures, label="Temperature", color='red', linestyle='--')

#     elif algorithm == 'hillclimber':
#         plt.title("Hill Climber: optimization of quality score K")

#     plt.xlabel("Iterations")
#     plt.ylabel("Quality Score (K)")
#     plt.grid(True)
#     plt.legend()

#     # Display the plot
#     plt.show()


# if __name__ == "__main__":
#     plot_hillclimb_sim_ann()
