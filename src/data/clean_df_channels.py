import pandas as pd
from sklearn.neighbors import NearestNeighbors
import numpy as np

def clean_data(input_file, output_file):
    # Load the TSV file
    df = pd.read_csv(input_file, compression="infer", sep='\t')
    
    # Drop rows with missing values in specified columns
    df_cleaned = df.dropna(subset=['category_cc', 'join_date', 'name_cc'])
    
    # Convert 'join_date' to datetime format
    df_cleaned['join_date'] = pd.to_datetime(df_cleaned['join_date'], errors='coerce')
    # Impute missing values in 'subscriber_rank_sb' based on similar 'subscribers_cc' values
    missing_rank_mask = df_cleaned['subscriber_rank_sb'].isnull()
    
    # Separate data with and without missing subscriber_rank_sb values
    data_with_rank = df_cleaned[~missing_rank_mask]
    data_without_rank = df_cleaned[missing_rank_mask]
    
    # Set up Nearest Neighbors model to find similar rows based on 'subscribers_cc'
    nn_model = NearestNeighbors(n_neighbors=5, algorithm='auto')
    nn_model.fit(data_with_rank[['subscribers_cc']])
    
    # Find nearest neighbors for rows with missing 'subscriber_rank_sb' based on 'subscribers_cc'
    distances, indices = nn_model.kneighbors(data_without_rank[['subscribers_cc']])
    
    # Impute missing 'subscriber_rank_sb' with the median rank of nearest neighbors
    imputed_ranks = []
    for idx_set in indices:
        neighbor_ranks = data_with_rank.iloc[idx_set]['subscriber_rank_sb'].values
        imputed_ranks.append(np.median(neighbor_ranks))
    
    # Assign the imputed values back to the original DataFrame
    df_cleaned.loc[missing_rank_mask, 'subscriber_rank_sb'] = imputed_ranks
    
    # Save the cleaned DataFrame to a new TSV file
    df_cleaned.to_csv(output_file, sep='\t', index=False)
    print(f"Cleaned data saved to {output_file}")


input_file = '../../data/df_channels.tsv.gz'
output_file = '../../data/df_channels_cleaned.tsv'
clean_data(input_file, output_file)

