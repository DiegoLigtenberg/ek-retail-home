import pandas as pd
from pathlib import Path

import pickle
# Load labels (translated)
with open('utils/brick_code_to_title.pkl', 'rb') as f:
    labels_list_translated = pickle.load(f)

print(labels_list_translated[10005215])
print(labels_list_translated[10001320])
asd

# Read the 'ground_truth_columbus_data.csv' file
ground_truth_data = pd.read_excel('ground_truth_columbus_data.xlsx')

# Select the desired columns from 'ground_truth_data'
ground_truth_data = ground_truth_data[['EAN', 'BrickCodeGroundTruth', 'BrickTitle']]

# Read the 'test_predictions_full.xlsx' file
test_predictions_data = pd.read_excel('test_predictions_full.xlsx')


# Extract basenames from 'image_file' and remove the file extensions
def extract_image_id(path):
    if isinstance(path, str):
        filename = Path(path).stem
        if '-' in filename or '-' in path:
            return "0"  # Exclude images with hyphens as a string
        if '_' in filename:
            return filename.split('_')[0]
        else:
            return filename
    return path

# Filter out images with hyphens
test_predictions_data['image_file'] = test_predictions_data['image_file'].apply(extract_image_id)

# Convert 'image_file' to numeric data type
test_predictions_data['image_file'] = pd.to_numeric(test_predictions_data['image_file'])

# Set a custom formatting option to display large numbers as integers
pd.options.display.float_format = '{:.0f}'.format


ground_truth_data['EAN'] = ground_truth_data['EAN'].str.replace(',00', '')


# Convert the 'EAN' values to integers
ground_truth_data['EAN'] = ground_truth_data['EAN'].apply(lambda x: int(float(x)))

# print(len(test_predictions_data))
# asd

# Select the desired columns from 'test_predictions_data'
test_predictions_data = test_predictions_data[['image_file', 'BrickCode', 'BrickTitle', 'AltCode1', 'AltCode2', 'AltCode3', 'AltCode4']]


# Merge the two DataFrames on the 'EAN' column, including the additional columns
merged_data = pd.merge(ground_truth_data, test_predictions_data, left_on='EAN', right_on='image_file', how='inner').drop_duplicates()

# print(merged_data)
# print(ground_truth_data)
# # print(len(ground_truth_data))
# asd
# asd
# Select the desired columns
result_data = merged_data[['EAN', 'image_file', 'BrickCodeGroundTruth', 'BrickCode','AltCode1','AltCode2', 'AltCode3', 'AltCode4']]
# Convert 'image_file' column to integer
result_data['image_file'] = result_data['image_file'].astype(str)
# Print the resulting DataFrame
# print(result_data)

correct_classifications = 0  # Initialize a counter for correct classifications
total_rows = len(result_data)  # Total number of rows in the DataFrame

correct_rows = []  # List to store the rows with correct classifications

for index, row in result_data.iterrows():
    brick_code_ground_truth = row['BrickCodeGroundTruth']
    brick_code = row['BrickCode']
    alt_code1 = row['AltCode1']
    alt_code2 = row['AltCode2']
    alt_code3 = row['AltCode3']
    alt_code4 = row['AltCode4']

    if (
        brick_code_ground_truth == brick_code
        or brick_code_ground_truth == alt_code1
        or brick_code_ground_truth == alt_code2
        or brick_code_ground_truth == alt_code3
        or brick_code_ground_truth == alt_code4
    ):
        correct_rows.append(index)
        correct_classifications+=1

correct_data = result_data.loc[correct_rows]
print("Rows with correct classification:")
print(correct_data)

accuracy = correct_classifications / total_rows
print(f"Accuracy: {accuracy * 100:.2f}%")
print(f'correct matching rows:\t{(correct_classifications)}')
print(f'total matching rows:\t{(total_rows)}')

import pickle
# Load labels (translated)
with open('utils/brick_code_to_title.pkl', 'rb') as f:
    labels_list_translated = pickle.load(f)

print(labels_list_translated[10005215])
print(labels_list_translated[10002249])
# 11120254471