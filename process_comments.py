import pandas as pd
import warnings
import pandas as pd

# Ignorer tous les warnings
warnings.filterwarnings("ignore")


def filter_df(df, N) : 

    # Créer une colonne 'group' qui marque les groupes d'auteurs consécutifs
    df['group'] = (df['author'] != df['author'].shift()).cumsum()

    # Compter la taille de chaque groupe
    group_sizes = df.groupby('group').size()

    # Sélectionner les groupes qui ont une taille supérieure à N
    valid_groups = group_sizes[group_sizes > N].index

    # Filtrer le DataFrame pour garder uniquement les lignes des groupes valides
    filtered_df = df[df['group'].isin(valid_groups)]
    result = filtered_df.groupby('author')['video_id'].apply(lambda x: ', '.join(x)).reset_index()

    return result



def main():
    print("-----START-----")
    output_file = "filtered_comments.csv"  # Nom du fichier de sortie
    N = 50
    n = 1000000
    i = 0

    # Initialiser une première écriture pour inclure les en-têtes
    first_write = True

    while True: 
        try:
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
                mode='w' if first_write else 'a',  # 'w' pour écraser au début, 'a' pour ajouter ensuite
                index=False, 
                header=first_write  # Inclure l'en-tête seulement lors de la première écriture
            )

            first_write = False  # Les écritures suivantes n'incluront pas l'en-tête

            # Afficher la progression
            print(f"{(i * n / 7e9) * 100:.2f} %", end='\r')

            i += 1

        except StopIteration:
            break

    print("\nTraitement terminé !")


if __name__ == "__main__":
    main()
