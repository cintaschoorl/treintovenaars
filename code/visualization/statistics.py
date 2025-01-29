import json
import matplotlib.pyplot as plt
import os

def plot_quality_score_histogram(json_file: json, algorithm: str, region: str):
    """
    Plots a histogram of quality scores for Random and Random Greedy algorithms.
    
    Input:
        - json_file (json): path to the JSON file containing quality scores
        - algorithm (str): name of the algorithm (for title and file naming)
        - region (str): name of the region (Holland or Netherlands) for correct saving
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
        - region (str): name of the region (Holland or Netherlands) for correct saving
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
