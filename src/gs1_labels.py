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

# Create a lookup table where 'BrickTitle' is the key and the row data is the value
brick_title_to_code = {}
brick_code_to_title = {}  # New dictionary to map BrickCode to BrickTitle

for index, row in df.iterrows():
    brick_title = row['BrickTitle']
    row_data = {
        'SegmentCode': row['SegmentCode'],
        'SegmentTitle': row['SegmentTitle'],
        'FamilyCode': row['FamilyCode'],
        'FamilyTitle': row['FamilyTitle'],
        'ClassCode': row['ClassCode'],
        'ClassTitle': row['ClassTitle'],
        'BrickCode': row['BrickCode'],
    }
    brick_title_to_code[brick_title] = row_data
    brick_code = row['BrickCode']
    brick_title = row['BrickTitle']
    brick_code_to_title[brick_code] = brick_title  # Map BrickCode to BrickTitle

# Save the lookup_table to a pickle file
with open('utils/brick_title_to_code.pkl', 'wb') as file:
    pickle.dump(brick_title_to_code, file)

# Save the BrickCode to BrickTitle mapping to a separate pickle file
with open('utils/brick_code_to_title.pkl', 'wb') as file:
    pickle.dump(brick_code_to_title, file)

if __name__ == "__main__":
    brick_title_value = "Adhesive Paste/Glue Removers"
    if brick_title_value in brick_title_to_code:
        associated_data = brick_title_to_code[brick_title_value]
        print(associated_data)
    else:
        print(f"'{brick_title_value}' not found in the lookup table.")

    brick_code_value = 10005444.0  # Replace with the desired BrickCode
    if brick_code_value in brick_code_to_title:
        brick_title = brick_code_to_title[brick_code_value]
        print(f"BrickTitle for BrickCode {brick_code_value}: {brick_title}")
    else:
        print(f"BrickCode '{brick_code_value}' not found in the mapping.")
