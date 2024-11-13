import pandas as pd

def clean_timeseries_data(input_file, output_file):
    df = pd.read_csv(input_file, sep="\t")
    
    # Step 1: Convert datetime column to datetime format and normalize time to midnight
    df['datetime'] = pd.to_datetime(df['datetime']).dt.normalize()
    
    # Step 2: Forward and backward fill NaN values in the category column.
    # This is a good idea since the category of a time series is likely to remain the same for a period of time.
    df['category'] = df['category'].ffill().bfill()
    
    # Save the cleaned DataFrame to a new TSV file
    df.to_csv(output_file, sep='\t', index=False)
    print(f"Cleaned data saved to {output_file}")


input_file = '../../data/df_timeseries_en.tsv'
output_file = '../../data/df_timeseries_en_cleaned.tsv'
clean_timeseries_data(input_file, output_file)
