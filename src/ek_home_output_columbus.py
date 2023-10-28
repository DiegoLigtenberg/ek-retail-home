import pandas as pd
import shutil
from pathlib import Path

# Read the Excel file
excel_file = 'test_predictions_full.xlsx'
df = pd.read_excel(excel_file)

# Specify the input and output directories
output_dir = Path('output/columbus')  # Change this to your output directory

# Create the output directory if it doesn't exist
output_dir.mkdir(parents=True, exist_ok=True)

# Loop through all 4 kategories
# for i in range(1):
    # Loop through the rows in the DataFrame
for index, row in df.iterrows():
    image_file = row['image_file']  # Assuming the column name is 'image_file'
    kategorie_i = row[f'BrickTitle']  # Replace 'Kategorie 2' with the actual column name
    kategorie_i = kategorie_i.replace('/','-')

    # Construct the source and destination paths
    source_path = image_file
    destination_path = output_dir / Path(kategorie_i) / Path(image_file).name

    # Create the subcategory folder if it doesn't exist
    destination_path.parent.mkdir(parents=True, exist_ok=True)
    print(destination_path)
    # asd
    # Copy the image file
    shutil.copy(source_path, destination_path)

    print(f"Copied {image_file} to {destination_path}",end='\r')

print("Image copying complete.")
