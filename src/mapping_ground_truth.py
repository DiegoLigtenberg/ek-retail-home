import pandas as pd
import pickle
import io

'''
some files have a wg/wug combination that corresponds to a brick title, but which is not found in the AI active labels 
some wg/wug combinations relate to the same brick title 
-> this means that there are less unique brick titles in ground truth set
'''

# Load your CSV file
excel_file = 'columbus_data.csv'

# Initialize an empty list to store DataFrames
data_frames = []

# List to store the indices of rows with non-UTF-8 characters
rows_to_remove = []

# Read the CSV file line by line, skipping rows with non-UTF-8 characters
with open(excel_file, 'r', encoding='utf-8', errors='replace') as file:
    first_line = True  # Flag to indicate the first line (header)
    for index, line in enumerate(file):
        if first_line:
            # Use the first line as the header
            columns = line.strip().split(';')
            column_indices = [columns.index(col) for col in ['EAN', 'WG', 'WUG']]
            first_line = False
        else:
            try:
                # Specify the correct delimiter (semicolon) and select specific columns
                data = pd.read_csv(io.StringIO(line), header=None, delimiter=';', usecols=column_indices)
                data_frames.append(data)
            except pd.errors.ParserError:
                rows_to_remove.append(index)
      

# Now, remove rows with non-UTF-8 characters
df = pd.concat(data_frames, axis=0, ignore_index=True)

# Set the column names explicitly
df.columns = ['EAN', 'WG', 'WUG']

# Load the translation table for BrickCodeGroundTruth
with open('utils/wg_wug_to_brick.pkl', 'rb') as file:
    wg_wug_to_brick_translation_table = pickle.load(file)

with open('utils/brick_code_to_title.pkl', 'rb') as file:
    lookup_table = pickle.load(file)

# Map the WG and WUG combinations to Brick Code Ground Truth
df['BrickCodeGroundTruth'] = df.apply(lambda row: wg_wug_to_brick_translation_table.get((row['WG'], row['WUG']), None), axis=1)

# Create a new column 'BrickTitle' based on the lookup table
df['BrickTitle'] = df['BrickCodeGroundTruth'].map(lookup_table)

df = df.dropna()
# Save the updated DataFrame to a new CSV file
df.to_excel('ground_truth_columbus_data.xlsx', index=False)

print(df)