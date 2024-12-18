######################################################
# This script creates several csv fail


import pandas as pd
import warnings
import pandas as pd





# Ignorer tous les warnings
warnings.filterwarnings("ignore")


def filter_df(df, N):
    df['group'] = (df['author'] != df['author'].shift()).cumsum()
    group_sizes = df.groupby('group')['author'].transform('size')
    df_filtered = df[group_sizes > N]
    result = df_filtered.groupby('author')['video_id'].apply(lambda x: ', '.join(x)).reset_index()
    return result







def main():
    print("-----START-----")
     # Nom du fichier de sortie
    N = 100
    n = 100_000_000
    i = 0



    while True: 
        try:
            output_file = "filtered_comments_" + str(i) + ".csv" 
            # Lire un chunk de données
            df_sample_comments = pd.read_csv(
                "youtube_comments.tsv.gz",
                compression="infer",
                sep="\t", 
                nrows=n, 
                skiprows=range(1, n * i),
                usecols=[0, 1],
                names=["author", "video_id"],  # Nommer les colonnes
                header=0 if i == 0 else None  # Inclure l'en-tête seulement pour le premier chunk
            )

            if df_sample_comments.empty:  # Arrêter la boucle si le chunk est vide
                break


            # Filtrer les données
            filtered_comments_df = filter_df(df_sample_comments, N)

            # Écrire les données filtrées dans le fichier CSV
            filtered_comments_df.to_csv(
                output_file, 
                mode='w' ,  # 'w' pour écraser au début, 'a' pour ajouter ensuite
                index=False, 
                header=None  # Inclure l'en-tête seulement lors de la première écriture
            )
            i += 1

            # Afficher la progression
            print(f"{(i * n / 8e9) * 100:.2f} %", end='\r')



        except StopIteration:
            break

    print("\nTraitement terminé !")


if __name__ == "__main__":
    main()
