#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec 13 19:56:52 2024
@author: valentinerehn
"""


import pandas as pd
import os

def process_chunk(chunk, keywords):
    """Process a single chunk of YouTube metadata."""
    # Filter out rows with NaN values
    valid_rows = chunk.dropna(subset=['channel_id', 'categories', 'description'])
    
    if len(valid_rows) == 0:
        return None
        
    # Initialize dictionary for the new rows
    new_rows = {
        'channel_id': valid_rows['channel_id'],
        'category_cc': valid_rows['categories']
    }
    
    # Convert descriptions to lowercase for case-insensitive matching
    descriptions = valid_rows['description'].str.lower()
    
    # Process each keyword - only keeping the binary flags
    for keyword in keywords:
        keyword_lower = keyword.lower()
        new_rows[f'has_{keyword}'] = descriptions.str.contains(keyword_lower, regex=False).astype(int)
    
    # Create DataFrame for this chunk and drop invalid rows
    df_chunk = pd.DataFrame(new_rows)
    return df_chunk.dropna(subset=['channel_id', 'category_cc'])

def get_metadata_analysis(data_path, chunk_size):
    """Analyze YouTube metadata for keyword presence."""
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
    
    # Handle duplicates by keeping the first occurrence
    return combined_df.drop_duplicates(subset=['channel_id'], keep='first')

def get_monetization_data(data_path):
    """Load and process monetization data."""
    clean_channel_monetization = pd.read_csv(
        os.path.join(data_path, "clean_channel_monetization.csv"),
        sep=","
    )
    
    return clean_channel_monetization[
        ['channel_id', 'category_cc', 'has_affiliate', 'has_sponsorships', 'has_merchandise']
    ]

def create_cross_analysis(data_path, output_filename, chunk_size=20000):
    """
    Create cross-analysis of YouTube metadata and monetization data.
    
    Parameters:
    -----------
    data_path : str
        Path to the directory containing input files
    output_filename : str
        Name of the output CSV file
    chunk_size : int, optional
        Size of chunks for processing large files (default: 20000)
    """
    # Get keyword analysis DataFrame (now with duplicates removed)
    keyword_df = get_metadata_analysis(data_path, chunk_size)
    
    # Get monetization data
    channel_sub = get_monetization_data(data_path)
    
    # Merge the DataFrames with inner join
    merged_df = pd.merge(
        keyword_df,
        channel_sub,
        on='channel_id',
        how='inner'
    )
    
    # Clean up merged DataFrame
    merged_df = merged_df.drop('category_cc_y', axis=1).rename(columns={'category_cc_x': 'category_cc'})
    
    # Save category value counts before grouping
    category_counts = merged_df['category_cc'].value_counts()
    category_counts.to_csv(os.path.join(data_path, 'sizes.csv'))
    
    # Group by categories and sum all flag columns
    category_sums = merged_df.groupby('category_cc').sum(numeric_only=True).reset_index()
    
    # Save results to CSV
    output_path = os.path.join(data_path, output_filename)
    category_sums.to_csv(output_path, index=False)
    
    return category_sums, merged_df


data_path = 'datasets'
output_filename = 'df_cross_analysis.csv'
category_sums, merged_df = create_cross_analysis(data_path, output_filename)