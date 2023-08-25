
from scipy.stats import pearsonr
import pandas as pd
import sys
import numpy as np
import os

# Function to read the number of items in a text file
def read_length_txt(filename):
    with open(filename, 'r') as f:
        lines = f.readlines()
        num_items = len(lines)
        print(f"The number of items in {filename} is: {num_items}")
    return num_items

# Function to create a DataFrame from a txt file, only reads txt files 
def create_df(filename):
  if filename.endswith('.txt'): 
    return pd.read_csv(filename)
  else:
    return None

# Function to convert DataFrame into a flattened list
def create_list(df):
    return df.values.flatten()

# Function to calculate the Pearson correlation coefficient
def pearson_calc(list1, list2):

#Zip the lists here to shorten the longer list down to the length of the shorter list
#this allows for pearson correlation 
    truncated_lists = list(zip(list1, list2))
    #print(truncated_lists)
    list1, list2 = zip(*truncated_lists)

    corr, _ = pearsonr(list1, list2)
    return corr

# Get a list of all the filenames in the current folder
folder_path = os.getcwd()
file_names = os.listdir(folder_path)
file_names = [os.path.join(folder_path, file) for file in file_names]

print(f'\n-correlating metric files from the path: \n\n {folder_path}')

print("\n=========CORRELATIONS=========")

# Correlate every file with every other file
for i, filename1 in enumerate(file_names):
    for filename2 in file_names[i+1:]:

        df1 = create_df(filename1)
        if df1 is None:
            continue 

        df2 = create_df(filename2)
        if df2 is None:
            continue

        list1 = create_list(df1)
        list2 = create_list(df2)

        corr_coefficient = pearson_calc(list1, list2)
        print(f"\nThe Pearson correlation between {os.path.basename(filename1)} and {os.path.basename(filename2)} is:\n {corr_coefficient:.3f}")

