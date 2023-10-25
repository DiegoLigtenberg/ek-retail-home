import pandas as pd
import pickle

# Replace 'GS1 classifications for EK Infinity (2).xlsx' with your actual file path
excel_file = 'GS1 classifications for EK Infinity (2).xlsx'

# Replace the column names with the ones you want to select
columns_to_select = ['SegmentCode', 'SegmentTitle', 'FamilyCode', 'FamilyTitle', 'ClassCode', 'ClassTitle', 'BrickCode', 'BrickTitle', 'AI Active']

# Specify the sheet name
sheet_name = 'GS1 Code Englisch'

# Read the specified columns from the 'GS1 Code Englisch' sheet into a DataFrame
df = pd.read_excel(excel_file, usecols=columns_to_select, header=1, sheet_name=sheet_name)

# Filter the DataFrame to include only rows where 'AI Active' is 'X'
df = df[df['AI Active'] == 'X']

# Extract the values from the 'BrickTitle' column into a list
brick_title_list = df['BrickTitle'].tolist()

# Save the list as a pickle file
brick_title_list_file = 'utils/brick_title_list.pkl'
with open(brick_title_list_file, 'wb') as file:
    pickle.dump(brick_title_list, file)
