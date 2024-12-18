#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec 13 16:47:07 2024
@author: valentinerehn
"""

import pandas as pd

def get_cleaned_professionalization_in_description(data_path, output_csv_path, chunk_size):
    
    # Terms to search
    keywords = ['http', 'ad', 'shop', 'support']

    # Set up CSV writing
    first_chunk = True
    
    # Process file in chunks
    chunk_iterator = pd.read_json(
        data_path + "/yt_metadata_en.jsonl.gz",
        lines=True,
        compression='gzip',
        chunksize=chunk_size
    )

    for chunk in chunk_iterator:
        # Filter out rows with NaN values
        valid_rows = chunk.dropna(subset=['upload_date', 'categories', 'description'])
        
        if len(valid_rows) == 0:
            continue

        # Initialize dictionary for the new rows
        new_rows = {
            'upload_date': pd.to_datetime(valid_rows['upload_date'], errors='coerce'),
            'category_cc': valid_rows['categories']
        }

        # Convert descriptions to lowercase for case-insensitive matching
        descriptions = valid_rows['description'].str.lower()

        # Process each keyword
        for keyword in keywords:
            keyword_lower = keyword.lower()
            new_rows[f'has_{keyword}'] = descriptions.str.contains(keyword_lower, regex=False).astype(int)
            new_rows[f'count_{keyword}'] = descriptions.str.count(keyword_lower)

        # Create DataFrame for this chunk and drop invalid rows
        df_chunk = pd.DataFrame(new_rows)
        df_chunk = df_chunk.dropna(subset=['upload_date', 'category_cc'])
        
        # Write to CSV
        if first_chunk:
            df_chunk.to_csv(output_csv_path, mode='w', index=False)
            first_chunk = False
        else:
            df_chunk.to_csv(output_csv_path, mode='a', header=False, index=False)
       

data_path = 'datasets'
output_csv_path = 'datasets/clean_professionalization_in_description.csv'
get_cleaned_professionalization_in_description(data_path,output_csv_path, 20000)
