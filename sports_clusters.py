# -*- coding: utf-8 -*-
"""
Created on Sat May 18 16:39:07 2024

@author: ricky
"""

from matplotlib.colors import ListedColormap
import pandas as pd
import re
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import umap
import seaborn as sns


# Read the CSV files
lemmatised_df = pd.read_csv(r'.\scopus\scopus_20k_lemmatised.csv')
sports_df = pd.read_csv(r'.\olympic_sports.csv')

# Extract the lemmatised texts and sports list
lemmatised_texts = lemmatised_df['lemmatized_text'].tolist()
sports_list = sports_df['Sports'].str.lower().tolist()

# Initialize a dictionary to hold clusters
clusters = {sport: [] for sport in sports_list}

# Preprocess texts to add spaces around non-word characters
preprocessed_texts = []
for text in lemmatised_texts:
    # Add space around non-word characters
    preprocessed_text = re.sub(r'(\W)', r' \1 ', text)
    preprocessed_texts.append(preprocessed_text)

# Check for the presence of each sport in each lemmatised text and assign clusters
for idx, text in enumerate(preprocessed_texts):
    for sport in sports_list:
        # Use regular expression to find whole words
        if re.search(r'\b' + re.escape(sport) + r'\b', text):
            clusters[sport].append(idx)

# Print the clusters
for sport, articles in clusters.items():
    print(f"Cluster for sport '{sport}':")
    print(articles)
    
    
    
# Bar Chart
sport_counts = {sport: len(articles) for sport, articles in clusters.items()}
plt.figure(figsize=(12, 6))
plt.bar(sport_counts.keys(), sport_counts.values())
plt.xticks(rotation=90)
plt.xlabel('Sports')
plt.ylabel('Number of Articles')
plt.title('Number of Articles per Sport')
plt.show()



# Heatmap
heatmap_data = np.zeros((len(lemmatised_texts), len(sports_list)))
for sport, articles in clusters.items():
    for idx in articles:
        sport_index = sports_list.index(sport)
        heatmap_data[idx, sport_index] = 1

# Create a custom color map with two colors
cmap = ListedColormap(['white', 'black'])

plt.figure(figsize=(15, 10))
sns.heatmap(heatmap_data, yticklabels=False, xticklabels=sports_list, cmap=cmap, cbar=False)
plt.title('Heatmap of Sports Presence in Articles')
plt.xlabel('Sports')
plt.ylabel('Articles')
plt.show()

# Prepare data for UMAP
presence_matrix = []
labels = []
for sport, articles in clusters.items():
    for idx in articles:
        presence_vector = [0] * len(sports_list)
        presence_vector[sports_list.index(sport)] = 1
        presence_matrix.append(presence_vector)
        labels.append(sport)

# Perform UMAP for visualization
umap_reducer = umap.UMAP(n_components=2, random_state=42)
umap_results = umap_reducer.fit_transform(presence_matrix)

# Create a scatter plot with each cluster having its own color
unique_labels = list(set(labels))
colors = plt.cm.get_cmap('tab20', len(unique_labels))

plt.figure(figsize=(12, 8))
for i, label in enumerate(unique_labels):
    indices = [j for j, lbl in enumerate(labels) if lbl == label]
    plt.scatter(umap_results[indices, 0], umap_results[indices, 1], color=colors(i), label=label, alpha=0.6)

plt.title('UMAP visualization of clusters based on sports presence')
plt.xlabel('UMAP feature 1')
plt.ylabel('UMAP feature 2')
plt.legend(loc='best')
plt.tight_layout()  
plt.show()