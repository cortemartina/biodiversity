
# For this project, you will interpret data from the National Parks Service 
# about endangered species in different parks. 
# You will perform some data analysis on the conservation statuses of these species 
# and investigate if there are any patterns or themes to the types of species that become endangered. 
# During this project, you will analyze, clean up, and plot data as well as pose questions 
# and seek to answer them in a meaningful way.

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

path = '/Users/martinacorte/Codecademy/Data Scientist/Projects/biodiversity_starter'
observations_data = pd.read_csv(f'{path}/observations.csv')
species_info_data = pd.read_csv(f'{path}/species_info.csv')

# print(observations_data.describe())
# print(observations_data.info())
# print(species_info_data.describe())
# print(species_info_data.info())

# What is the distribution of conservation_status for animals?
print(species_info_data.conservation_status.unique())
status_counts = species_info_data['conservation_status'].value_counts()
plt.figure(figsize=(8, 6))
sns.barplot(x=status_counts.index, y=status_counts.values, palette='viridis')
plt.title('Species Count by Conservation Status')
plt.xlabel('Conservation Status')
plt.ylabel('Number of Species')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
# Note: Out of a total of 5824 species, only 191 have a recorded conservation status. 
# The chart shows the distribution of these 191 species by conservation status category.

# Are certain types of species more likely to be endangered?
print(species_info_data.category.unique())
endangered_species = species_info_data[species_info_data['conservation_status'] == 'Endangered']
endangered_counts = endangered_species['category'].value_counts()
plt.figure(figsize=(8,6))
sns.barplot(x=endangered_counts.index, y=endangered_counts.values, palette='viridis')
plt.title('Species category endagered')
plt.xlabel('Species category')
plt.ylabel('Number of Species')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# Are the differences between species and their conservation status significant?
categories = species_info_data['category'].dropna().unique()
status_order = species_info_data['conservation_status'].dropna().unique()

fig, axes = plt.subplots(2, 4, figsize=(8,6))
axes = axes.flatten()
for i, category in enumerate(categories):
    ax = axes[i]
    subset = species_info_data[species_info_data['category'] == category]
    sns.countplot(data=subset, x='conservation_status', ax=ax, order=status_order, palette='viridis')
    ax.set_title(category)
    ax.set_xlabel('')
    ax.set_ylabel('Count')
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha='right')

for j in range(len(categories), len(axes)):
    fig.delaxes(axes[j])
plt.tight_layout()
plt.show()
# In every category (mammals, birds, reptiles, amphibians, fish, vascular and 
# nonvascular plants) the 'Species of Concern' is the most observed conservation_status. 
# For the Fish category, also 'Endangered' and 'Threatened' status have a similar value. 
# Reptiles, Vascular and Nonvascular plants have only 'Species of Concern' status.

# Which species were spotted the most at each park?
# Sort by park and observations descending
obs_sorted = observations_data.sort_values(['park_name', 'observations'], ascending=[True, False])

# Group by park and take top 5 species per park
top5_per_park = obs_sorted.groupby('park_name').head(5)

# Get unique parks
parks = top5_per_park['park_name'].unique()

fig, axes = plt.subplots(2, 2, figsize=(8,6))
axes = axes.flatten()

for i, park in enumerate(parks):
    ax = axes[i]
    data = top5_per_park[top5_per_park['park_name'] == park]

    # Sort species by observations for better bar ordering
    data = data.sort_values('observations', ascending=True)

    sns.barplot(x='observations', y='scientific_name', data=data, ax=ax, palette='viridis')

    ax.set_title(park)
    ax.set_xlabel('Observations')
    ax.set_ylabel('Species')

     # Dynamically set x-axis limits based on min and max of data
    min_obs = data['observations'].min()
    max_obs = data['observations'].max()
    
    buffer = (max_obs - min_obs) * 0.1  # add 10% space around the bars
    ax.set_xlim(min_obs - buffer, max_obs + buffer)

plt.tight_layout()
plt.show()