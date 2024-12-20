
################################################################
# This scripts reads the youtube_comments.tsv.gz 77GB file that contains auhtor of comments 
# and the id of the video they commented. It keeps only the authors who posted more than 100 comments
# and writes everything in a new csv file named filtered_comments.csv
################################################################

import pandas as pd
import warnings
import pandas as pd


# Ignores the warnings
warnings.filterwarnings("ignore")


def filter_df(df, N):
    """
    The goal of this function is to keep only tha authors who wrote more than N comments n the df dataframe.
    Returns a new dataframe filtered from the df dataframe. 
    """
    df['group'] = (df['author'] != df['author'].shift()).cumsum()
    group_sizes = df.groupby('group')['author'].transform('size')
    df_filtered = df[group_sizes > N]
    result = df_filtered.groupby('author')['video_id'].apply(lambda x: ', '.join(x)).reset_index()
    return result


def main():
    print("-----START-----")
    N = 100    # Minimum number of comments an author has to post to keep him
    n = 100_000_000    # Number of lines we read at each step
    i = 0   # Counter
    output_file = "filtered_comments" + ".csv"  # Creates a new csv file for each chunks
    while True: 
        try:
            df_sample_comments = pd.read_csv(
                "youtube_comments.tsv.gz",
                compression="infer",
                sep="\t", 
                nrows=n, 
                skiprows=range(1, n * i),
                usecols=[0, 1],
                names=["author", "video_id"],  
                header=0 if i == 0 else None  
            )  # Reads the csv file containing the comments 

            if df_sample_comments.empty:  # Stops the loop if the chunk is empty
                break

            filtered_comments_df = filter_df(df_sample_comments, N)  # Filters the data to keep only the relevant authors

            filtered_comments_df.to_csv( # Writes the data to the csv file 
            output_file, 
            mode='a' , 
            index=False, 
            header=None  
        )
            i += 1

            # Shows the progression
            print(f"{(i * n / 8e9) * 100:.2f} %", end='\r')

        except StopIteration:
            break
    

    print("\n---- Finished! ----")


if __name__ == "__main__":
    main()
