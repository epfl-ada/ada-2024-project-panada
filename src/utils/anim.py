###############################################################################
# This file creates the csv files we use for the flourish animation
# The csv files are the following : 
#   - similarities.csv that contains the similarities between the categories
#   - names.csv that contains the name of each category
###############################################################################


import pandas as pd
import numpy as np
import pickle
from chord import Chord


my_matrix = np.load("distance_matrix.npy")
matrix = 1 - my_matrix
my_matrix = matrix.tolist()
print(type(matrix))  


with open("liste_cat.pkl", "rb") as file:
    liste_categories = pickle.load(file)

names = liste_categories[:-2]
rows = []

for i in range(len(names)):
    for j in range(len(names)):
        if i != j:  
            rows.append([names[i], names[j], my_matrix[i][j]])

df = pd.DataFrame(rows, columns=["Catégorie 1", "Catégorie 2", "Nombre de commentateurs"])
df.to_csv("commentateurs_en_commun.csv", index=False, encoding="utf-8")
print("Fichier 'similarities.csv' généré avec succès.")

names = ['Film & Animation', 'Gaming', 'Education', 'People & Blogs', 'Entertainment',
         'Autos & Vehicles', 'Comedy', 'Sports', 'News & Politics', 'Music',
         'Howto & Style', 'Science & Technology', 'Travel & Events', 'Pets & Animals',
         'Nonprofits & Activism']

df = pd.DataFrame({"Index": range(len(names))}, index=names)
df.to_csv("names_indexed.csv", index_label="Name")
print("Fichier 'names.csv' généré avec succès.")