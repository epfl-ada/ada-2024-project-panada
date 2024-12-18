#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec 13 12:22:56 2024
@author: valentinerehn
"""

import pandas as pd
import os


def generate_clean_df_channels_en(data_path):

    
    # Step 1: Load the dataset and select relevant columns
    df_channels_en = pd.read_csv(
        os.path.join(data_path, "df_channels_en.tsv.gz"),
        compression="infer",
        sep="\t"
    )
    df_channels_en = df_channels_en[["category_cc", "channel"]]
    
    # Step 2: Remove rows with missing values
    df_cleaned = df_channels_en.dropna(axis=0, how='any', ignore_index=True)
    
    # Step 3: Identify channels that are duplicated
    duplicate_channels = df_cleaned[df_cleaned.duplicated(subset="channel", keep=False)]
    
    # Case 1: Keep one entry if 'category_cc' is the same for all duplicates
    same_category = duplicate_channels.groupby("channel").filter(
        lambda x: len(x["category_cc"].unique()) == 1
    ).drop_duplicates(subset="channel")
    
    # Case 2: Remove all entries if 'category_cc' differs for the same channel
    different_category = duplicate_channels.groupby("channel").filter(
        lambda x: len(x["category_cc"].unique()) > 1
    )
    
    # Step 4: Create the final cleaned DataFrame
    # - Keep rows that are not duplicates
    # - Add the rows from Case 1
    clean_df_channels_en = pd.concat([
        df_cleaned[~df_cleaned["channel"].isin(duplicate_channels["channel"])],
        same_category
    ])
    
    # Reset index for a clean final DataFrame
    clean_df_channels_en.reset_index(drop=True, inplace=True)
    
    return clean_df_channels_en

def generate_clean_monetization(data_path):
    
    # Step 1: Load the dataset
    monetization = pd.read_csv(
        os.path.join(data_path, "youtube_monetization_api.csv"),
        sep=","
    )
    
    # Remove rows with missing values
    monetization_cleaned = monetization.dropna(axis=0, how="any", ignore_index=True)
    
    # Step 2: Identify duplicate 'channel_id' entries
    duplicate_channels = monetization_cleaned[
        monetization_cleaned.duplicated(subset="channel_id", keep=False)
    ]
    
    # Case 1: Keep one entry if all duplicates have the same associated data
    same_data = duplicate_channels.groupby("channel_id").filter(
        lambda x: len(x.drop_duplicates()) == 1
    ).drop_duplicates(subset="channel_id")
    
    # Case 2: Remove all entries if duplicates have conflicting data
    conflicting_data = duplicate_channels.groupby("channel_id").filter(
        lambda x: len(x.drop_duplicates()) > 1
    )
    
    # Step 3: Create the final cleaned DataFrame
    # - Keep rows that are not duplicated
    # - Add rows from Case 1
    clean_monetization = pd.concat([
        monetization_cleaned[~monetization_cleaned["channel_id"].isin(duplicate_channels["channel_id"])],
        same_data
    ])
    
    # Reset index for the cleaned DataFrame
    clean_monetization.reset_index(drop=True, inplace=True)
    
    return clean_monetization

def generate_clean_channel_monetization(data_path):
    
    # Step 1: Clean the datasets
    df_channels_en = generate_clean_df_channels_en(data_path)
    monetization = generate_clean_monetization(data_path)
    
    # Step 2: Merge the datasets
    merged_dataset = pd.merge(
        monetization, 
        df_channels_en, 
        left_on="channel_id", 
        right_on="channel"
    ).drop(columns=["channel"])  # Drop redundant 'channel' column

    # Step 3: Write the merged dataset to a CSV file
    output_path = os.path.join(data_path, "clean_channel_monetization.csv")
    merged_dataset.to_csv(output_path, index=False)

    print(f"Merged dataset successfully written to: {output_path}")

data_path = "datasets"
generate_clean_channel_monetization('datasets')

'''
share_merged = merged_dataset['category_cc'].value_counts(normalize = True)*100
category_cc
Entertainment            20.276420
Music                    17.110879
Gaming                   13.804019
People & Blogs           10.358667
Howto & Style            10.186258
Education                 6.582629
Film and Animation        4.779401
Comedy                    4.038891
Science & Technology      3.371866
Sports                    3.337950
Autos & Vehicles          2.006727
News & Politics           1.961505
Travel & Events           0.912919
Pets & Animals            0.887482
Nonprofits & Activism     0.384387

share_YN = df_channels_en['category_cc'].value_counts(normalize = True)*100 
category_cc
Music                    17.811826
Entertainment            16.833404
Gaming                   14.773877
People & Blogs           13.505009
Howto & Style             8.709715
Education                 5.723108
Film and Animation        5.042467
Sports                    3.775799
Science & Technology      3.567499
Comedy                    2.762905
Autos & Vehicles          2.717431
News & Politics           1.659797
Travel & Events           1.458831
Pets & Animals            0.947617
Nonprofits & Activism     0.710713
'''
