################################################################
# This scripts reads the yt_metadata_en.jsonl.gz 13GB file that contains metadata about each video
# It keeps only the relevant information for our analysis : 
#   - id of the video
#   - the category the video belongs to
# and writes everything in a new csv file named yt_metadata.csv
################################################################


import gzip
import json
import pandas as pd

def process_file() : 
    """
    Function that reads the json file and creates a dataframe containing only the relevant informations based on it.
    It finally writes the dataframe in csv file. 
    """
    data_list = []
    i = 0
    with gzip.open('yt_metadata_en.jsonl.gz', 'rt', encoding='utf-8') as file:  # Reading the json file
        for line in file:
            data = json.loads(line) 
            
            # Considers only the relevant information we need
            filtered_data = {
                'video_id': data.get('display_id'),
                'category': data.get('categories')
            }
            
            # adds filtered_data to a list
            data_list.append(filtered_data)
            i+=1
            print(f"{(i / 72924794) * 100:.2f} %", end='\r') # Shows the progression

    # Converts the list to a dataframe
    df_metadata = pd.DataFrame(data_list)

    print("---------- WRITING ----------")
    # Writes the datafrale to a csv file
    df_metadata.to_csv('yt_metadata.csv', mode='a', header=False, index=False)


if __name__ == "__main__":
    print("Start")
    process_file()
