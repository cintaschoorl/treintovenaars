import csv 
import matplotlib.pyplot as plt

# Visualize Random
def plot_random():
    pass 


# Visualize Hill Climber
def plot_hill_climber(csv_file="output/hillclimber_results.csv"):
    iterations = []
    scores = []

    # read CSV file
    with open(csv_file, 'r') as file:
        reader = csv.reader(file)
        next(reader)  # skip header

        for row in reader:
            iterations.append(int(row[0]))
            scores.append(int(row[1]))

    # create plot
    plt.figure(figsize=(10, 6))
    plt.plot(iterations, scores, label="Quality Score (K)", color='blue', marker='o')#, linestyle='-')

    plt.title("Hill Climber: optimization of quality score K")
    plt.xlabel("Iterations")
    plt.ylabel("Quality Score (K)")
    plt.grid(True)
    plt.legend()

    # Display the plot
    plt.show()


if __name__ == "__main__":
    plot_hill_climber()
    
