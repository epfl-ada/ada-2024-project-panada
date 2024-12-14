import gzip
import json
import pandas as pd

def process_file() : 
    # Initialisation d'une liste vide pour collecter les données
    data_list = []
    i = 0
    with gzip.open('yt_metadata_en.jsonl.gz', 'rt', encoding='utf-8') as file:
        for line in file:
            # Chaque ligne est un objet JSON
            data = json.loads(line)
            
            # Filtrer les informations dont tu as besoin
            filtered_data = {
                'video_id': data.get('display_id'),
                'category': data.get('categories')
            }
            
            # Ajouter filtered_data à la liste
            data_list.append(filtered_data)
            i+=1
            print(f"{(i / 72924794) * 100:.2f} %", end='\r')

    # Convertir la liste en DataFrame
    df_metadata = pd.DataFrame(data_list)
    print("---------- WRITING ----------")
    df_metadata.to_csv('yt_metadata.csv', mode='a', header=False, index=False)




if __name__ == "__main__":
    print("Start")
    process_file()
