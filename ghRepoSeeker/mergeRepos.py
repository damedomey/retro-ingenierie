import glob
import pandas as pd
import sys

print('Number of arguments:', len(sys.argv), 'arguments.')
print('Argument List:', str(sys.argv))

gitPRefix = ""
gitSuffix = ""

if len(sys.argv) == 2:
    if sys.argv[1] == "ssh":
        gitPRefix = "git@github.com:"
    elif sys.argv[1] == "https":
        gitPRefix = "https://github.com/"
    gitSuffix = ".git"

# Replace 'path/to/root/directory' with the path to your root directory
root_directory = '.'

# Search for all CSV files in the root directory
csv_files = glob.glob(f'{root_directory}/*.csv')

data_frames = []
for file_path in csv_files:
    df = pd.read_csv(file_path)
    df = gitPRefix + df + gitSuffix
    data_frames.append(df)

# Concatenate all DataFrames into one
combined_df = pd.concat(data_frames)

# Remove duplicates based on all columns
unique_combined_df = combined_df.drop_duplicates()

print("There is : ", len(unique_combined_df), " repositories")

# Replace 'output.csv' with the desired name for your merged file
output_file = 'allRepos.csv'

# Write the unique content to a new CSV file
unique_combined_df.to_csv(output_file, index=False)
