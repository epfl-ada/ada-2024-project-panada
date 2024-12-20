import pandas as pd
import numpy as np

def clean_feather(input_file, output_file):
    # Load the Feather file
    df = pd.read_feather(input_file)

    # 1. Handle missing values
    # Define a threshold for missing values in rows
    missing_threshold = 0.3  # Customize as needed

    # Drop rows with a high percentage of missing values
    df = df.dropna(thresh=int(df.shape[1] * (1 - missing_threshold)))

    # For remaining missing values, fill with column median for numeric columns
    for col in df.select_dtypes(include=np.number).columns:
        df[col].fillna(df[col].median(), inplace=True)

    # Fill missing values in categorical columns with the mode
    for col in df.select_dtypes(include='object').columns:
        df[col].fillna(df[col].mode()[0], inplace=True)

    # 2. Convert columns to appropriate data types
    # Convert 'upload_date' to datetime format
    df['upload_date'] = pd.to_datetime(df['upload_date'], errors='coerce')

    # Convert other columns to numeric if they are not already
    numeric_cols = ['dislike_count', 'duration', 'like_count', 'view_count']
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors='coerce')

    # 3. Handle negative values in numeric columns
    for col in numeric_cols:
        # Replace negative values with NaN and then fill them with column median
        df[col] = df[col].apply(lambda x: x if x >= 0 else np.nan)
        df[col].fillna(df[col].median(), inplace=True)

    # 4. Finalize cleaning by dropping any rows with still-missing data
    df.dropna(inplace=True)

    # Save the cleaned DataFrame to a new Feather file
    df.to_feather(output_file)
    print(f"Cleaned data has been saved to {output_file}")


#clean_feather('../../data/yt_metadata_helper.feather', '../../data/yt_metadata_cleaned.feather')
