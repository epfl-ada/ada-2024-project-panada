import pandas as pd

def remove_missing_comments(input_file, output_file):
    # Load the CSV file
    df = pd.read_csv(input_file, sep='\t')
    
    # Remove rows where 'num_comms' is missing
    df_cleaned = df.dropna(subset=['num_comms'])
    
    # Save the cleaned DataFrame to a new file
    df_cleaned.to_csv(output_file, sep='\t', index=False)
    print(f"Cleaned data saved to {output_file}")

# Usage
input_file = 'data/num_comments.tsv'
output_file = 'data/num_comments_cleaned.tsv'
remove_missing_comments(input_file, output_file)
