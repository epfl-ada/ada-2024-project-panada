import pandas as pd
import numpy as np

import pickle

print("----IMPORTING METADATA----")
df_metadata = pd.read_csv("yt_metadata.csv")

new_row = ['video_id', 'category']

# Ajouter la nouvelle ligne en haut du DataFrame
df_metadata.loc[-1] = new_row  # Ajouter la ligne à l'index -1 (le début)
df_metadata.index = df_metadata.index + 1  # Décaler les index pour éviter d'écraser les données
df_metadata = df_metadata.sort_index()  # Réordonner les index

# Maintenant, la première ligne devient les noms des colonnes
df_metadata.columns = df_metadata.iloc[0]  # Utiliser la première ligne comme noms de colonnes
df_metadata = df_metadata.drop(0)  # Supprimer la première ligne maintenant qu'elle est devenue les noms de colonnes

df_metadata.dropna(inplace=True)

dict_metadata = dict(zip(df_metadata['video_id'], df_metadata['category']))

liste_categories = df_metadata["category"].unique()


# Sauvegarde dans un fichier
with open("liste_cat.pkl", "wb") as fichier:  # "wb" = write binary
    pickle.dump(liste_categories, fichier)

print("----CATEGORIES UPLOADED INTO PICKLE FILE----")


N_cat = len(liste_categories)

filtered_comments = pd.read_csv("filtered_comments.csv")

matrix = np.zeros((len(filtered_comments), len(liste_categories)))

def dict_from_list(liste):
    return {element: index for index, element in enumerate(liste)}

index_cate = dict_from_list(liste_categories)


def parse_video_id(my_list_str, matrix, i) : 
    liste_id = my_list_str.split(", ")
    for element in liste_id : 
        cat = dict_metadata.get(element, None)
        if cat is not None : 
            matrix[i, index_cate[cat]] += 1

print("----CREATING MATRIX---\n\n")
i = 0
for row in filtered_comments.itertuples():
    print(f"{i/len(filtered_comments) * 100:.2f} %%", end = "\r")
    parse_video_id(row.video_id, matrix, i)
    matrix[i] = matrix[i]
    i+=1
print(f"{i/len(filtered_comments) * 100:.2f} %%")

np.save("my_matrix.npy", matrix)

