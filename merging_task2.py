from matplotlib.dates import DateFormatter, YearLocator
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
import os
import pickle


print("---- READING DATASET COMMENTS ----")
df_num_comments = pd.read_csv("num_comments.tsv.gz", compression = "infer", sep = "\t")
df_num_comments.dropna(inplace = True)
print("---- READING DATASET METADATA ----")
df_metadata_task2 = pd.read_csv("yt_metadata_task2.csv", names=['video_id', 'category', 'dislike_count', 'like_count', 'view_count', 'duration', 'upload_date'])
df_metadata_task2.dropna(inplace=True)

print("---- MERGING DATASETS ----")
merged_df = pd.merge(df_num_comments, df_metadata_task2, how='inner', left_on = "display_id", right_on = "video_id")

print("---- WRITING DATASET ----")
merged_df.to_csv('merged_task2.csv', index=False) 