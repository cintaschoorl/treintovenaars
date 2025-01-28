import csv
import matplotlib.pyplot as plt
import pandas as pd
import os

# Visualize Random
def plot_random(input_file):
    output_path = '../../output/quality_scores_histogram.png'
    # Lees de CSV file
    df = pd.read_csv(input_file)

    # Maak het histogram
    plt.figure(figsize=(10, 6))
    plt.hist(df['quality_score'], bins=20, edgecolor='black')
    plt.title('Distribution of Quality Scores (K) for Random Algorithm')
    plt.xlabel('Quality Score (K)')
    plt.ylabel('Frequency')

    # Voeg gemiddelde en standaarddeviatie toe aan de plot
    mean = df['quality_score'].mean()
    std = df['quality_score'].std()
    plt.axvline(mean, color='red', linestyle='dashed', linewidth=1)
    plt.text(mean*1.1, plt.ylim()[1]*0.9, f'Mean: {mean:.2f}\nStd: {std:.2f}')

    # Sla de plot op
    plt.savefig('output/quality_scores_histogram.png')
    plt.show()


# visualize random greedy
def plot_random_greedy(input_file):
    """
    Visualizing the distribution of quality scores from the random greedy algorithm.
    """
    df = pd.read_csv(input_file)

    # Creating the histogram
    plt.figure(figsize=(10, 6))
    plt.hist(df['quality_score'], bins=20, edgecolor='black', alpha=0.75)
    plt.title('Distribution of Quality Scores for Random Greedy Algorithm')
    plt.xlabel('Quality Score (K)')
    plt.ylabel('Frequency')

    # Adding the mean and the standard deviation values to the plot
    mean = df['quality_score'].mean()
    std = df['quality_score'].std()
    plt.axvline(mean, color='red', linestyle='dashed', linewidth=1)
    plt.text(mean * 1.05, plt.ylim()[1] * 0.9, f'Mean: {mean:.2f}\nStd: {std:.2f}', color='red')

    # Plotting 
    plt.savefig('output/quality_scores_histogram.png')
    plt.show()




# Visualize Hill Climber or Simulated Annealing
def plot_hillclimb_sim_ann(csv_file="output/hillclimber_results.csv", algorithm='hillclimber'):
    """
    Plots the course of the quality function K to the iterations.

    Input:
        - csv_file (.csv): iterations in the first row and K in the second
        - algorithm (str): choose which algorithm to plot: 'hillclimber' / 'sim_ann'

    """
    iterations = []
    scores = []
    temperatures = []

    # read CSV file
    with open(csv_file, 'r') as file:
        reader = csv.reader(file)
        next(reader)  # skip header

        for row in reader:
            iterations.append(int(row[0]))
            scores.append(int(row[1]))
            if algorithm == "sim_ann":
                temperatures.append(float(row[2]))

     # create plot
    plt.figure(figsize=(10, 6))
    plt.plot(iterations, scores, label="Quality Score (K)", color='blue', marker='o')  # Quality scores

    if algorithm == 'sim_ann':
        plt.title("Simulated Annealing: optimization of quality score K")
        # plot temperatures as a red line
        plt.plot(iterations, temperatures, label="Temperature", color='red', linestyle='--')

    elif algorithm == 'hillclimber':
        plt.title("Hill Climber: optimization of quality score K")

    plt.xlabel("Iterations")
    plt.ylabel("Quality Score (K)")
    plt.grid(True)
    plt.legend()

    # Display the plot
    plt.show()


if __name__ == "__main__":
    plot_hillclimb_sim_ann()
