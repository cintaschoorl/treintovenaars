import pandas as pd
import matplotlib.pyplot as plt
import os

output_path = '../../output/quality_scores_histogram.png'
# Sla het histogram op
plt.savefig(output_path)
plt.close()

file_path = '../../output/random_results.csv'
# Lees de CSV file
df = pd.read_csv(file_path)

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

# Print statistieken
print(f"\nStatistics:")
print(f"Mean: {mean:.2f}")
print(f"Std: {std:.2f}")
print(f"Min: {df['quality_score'].min():.2f}")
print(f"Max: {df['quality_score'].max():.2f}")
