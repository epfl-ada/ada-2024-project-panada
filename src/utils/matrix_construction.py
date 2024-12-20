############################################################################################################################
# THis python script does the following : 
# Using the "matrix_contruction.py" file, we open the "filtered_comments_i.csv" and 
# "yt_metadata.csv" files and we create based on them a matrix. Each row of the matrix 
# represents an author and each column a category. Noting the matrix $A$, then $A_{ij}$ would be 
# the number of comments the author i wrote unders videos belonging to the category j. 
# The matrix is then stored in the "my_matrix.npy" file.
############################################################################################################################



import pandas as pd
import numpy as np

import pickle

print("----IMPORTING METADATA----")
df_metadata = pd.read_csv("yt_metadata.csv")     # Reads the cleaned metadata.csv file

# There are no names for the columns in the dataframe so we replace the first row with the names of the columns
new_row = ['video_id', 'category']
df_metadata.loc[-1] = new_row  
df_metadata.index = df_metadata.index + 1  
df_metadata = df_metadata.sort_index()  
df_metadata.columns = df_metadata.iloc[0]  
df_metadata = df_metadata.drop(0)  

# Dropping the Nan values in the dataset
df_metadata.dropna(inplace=True)

# Creating a dictionnary based on the dataset. The keys are the video id's and the values are the categories associated woth the video 
dict_metadata = dict(zip(df_metadata['video_id'], df_metadata['category']))

# Liste des catégories dans le dataset
liste_categories = df_metadata["category"].unique()
with open("liste_cat.pkl", "wb") as fichier: # Saves the list of categories in a pickle file 
    pickle.dump(liste_categories, fichier)


print("----CATEGORIES UPLOADED INTO PICKLE FILE----")

N_cat = len(liste_categories) # Number of categories
filtered_comments = pd.read_csv("filtered_comments.csv")  # Reads the cleaned dataset 
matrix = np.zeros((len(filtered_comments), len(liste_categories)))  # Creating the matrix

def dict_from_list(liste):
    """
    This function creates a dictionnary where the keys are the elements of the list and the values are
    the index of the elements of the list
    Example : 

    param : iste = ["Adam", "Koami", "Valentine"]
    return : {"Adam" : 0, "Koami" : 1, "Valentine" : 2}
    """
    return {element: index for index, element in enumerate(liste)} 

index_cate = dict_from_list(liste_categories) # Creates a dictionnary based on the category 

def parse_video_id(my_list_str, matrix, i) : 
    """
    This function modifies the matrix names matrix based on the information in my_list_str. 
    """
    liste_id = my_list_str.split(", ")
    for element in liste_id : 
        cat = dict_metadata.get(element, None)
        if cat is not None : 
            matrix[i, index_cate[cat]] += 1

print("----CREATING MATRIX---\n\n")

# Modifies the matrix using the functions wrote just ahead

i = 0
for row in filtered_comments.itertuples():
    print(f"{i/len(filtered_comments) * 100:.2f} %%", end = "\r")
    parse_video_id(row.video_id, matrix, i)
    matrix[i] = matrix[i]
    i+=1
print(f"{i/len(filtered_comments) * 100:.2f} %%")

np.save("my_matrix.npy", matrix)  # Saving the matrix to use it in a notebook

