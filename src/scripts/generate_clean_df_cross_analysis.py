#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec 13 19:56:52 2024
@author: valentinerehn
"""


import pandas as pd
import os

def process_chunk(chunk, keywords):

    # Remove NaN
    valid_rows = chunk.dropna(subset=['channel_id', 'categories', 'description'])
    
    if len(valid_rows) == 0:
        return None
        
    # Dictionary for the new rows
    new_rows = {
        'channel_id': valid_rows['channel_id'],
        'category_cc': valid_rows['categories']
    }
    
    # Convert descriptions to lowercase 
    descriptions = valid_rows['description'].str.lower()
    
    # Process keywords
    for keyword in keywords:
        keyword_lower = keyword.lower()
        new_rows[f'has_{keyword}'] = descriptions.str.contains(keyword_lower, regex=False).astype(int)
    
    # Create DataFrame for this chunk and drop invalid rows
    df_chunk = pd.DataFrame(new_rows)
    return df_chunk.dropna(subset=['channel_id', 'category_cc'])

def get_metadata_analysis(data_path, chunk_size):

    keywords = ['http', 'ad', 'shop', 'support']
    all_chunks = []
    
    # Process file in chunks
    chunk_iterator = pd.read_json(
        os.path.join(data_path, "yt_metadata_en.jsonl.gz"),
        lines=True,
        compression='gzip',
        chunksize=chunk_size
    )
    
    for chunk in chunk_iterator:
        processed_chunk = process_chunk(chunk, keywords)
        if processed_chunk is not None:
            all_chunks.append(processed_chunk)
    
    # Combine all chunks
    combined_df = pd.concat(all_chunks, ignore_index=True)
    
    #Only keep the first occurrence
    return combined_df.drop_duplicates(subset=['channel_id'], keep='first')

def get_monetization_data(data_path):

    clean_channel_monetization = pd.read_csv(
        os.path.join(data_path, "clean_channel_monetization.csv"),
        sep=","
    )
    
    return clean_channel_monetization[
        ['channel_id', 'category_cc', 'has_affiliate', 'has_sponsorships', 'has_merchandise']
    ]

def create_cross_analysis(data_path, output_filename, chunk_size=20000):

    # Get keyword analysis DataFrame (duplicates removed)
    keyword_df = get_metadata_analysis(data_path, chunk_size)
    
    # Get monetization data
    channel_sub = get_monetization_data(data_path)
    
    # Merge channels and API data along categories
    merged_df = pd.merge(
        keyword_df,
        channel_sub,
        on='channel_id',
        how='inner'
    )
    
    # Drop duplicated category column
    merged_df = merged_df.drop('category_cc_y', axis=1).rename(columns={'category_cc_x': 'category_cc'})
    
    # Get the counts in a separated csv to normalize following data when plotting
    category_counts = merged_df['category_cc'].value_counts()
    category_counts.to_csv(os.path.join(data_path, 'sizes.csv'))
    
    # Group by categories and sum all columns of interest
    category_sums = merged_df.groupby('category_cc').sum(numeric_only=True).reset_index()
    
    # To CSV
    output_path = os.path.join(data_path, output_filename)
    category_sums.to_csv(output_path, index=False)
    
    return category_sums, merged_df


data_path = 'datasets'
output_filename = 'df_cross_analysis.csv'
category_sums, merged_df = create_cross_analysis(data_path, output_filename)