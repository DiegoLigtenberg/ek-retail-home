import pandas as pd
import pickle

# Load your Excel file
excel_file = 'MappingColumbus_400543847.xlsx'
df = pd.read_excel(excel_file, usecols=['WG', 'WUG', 'Brick Code'])


# Create a translation table from WG and WUG to Brick Code
wg_wug_to_brick_translation_table = df.drop_duplicates(subset=['WG', 'WUG']).set_index(['WG', 'WUG'])['Brick Code'].to_dict()

# Create a reverse translation table from Brick Code to WG and WUG
brick_to_wg_wug_translation_table = df.drop_duplicates(subset=['Brick Code']).set_index('Brick Code')[['WG', 'WUG']].to_dict(orient='index')

# Save the translation tables to pickle files
with open('utils/wg_wug_to_brick.pkl', 'wb') as f:
    pickle.dump(wg_wug_to_brick_translation_table, f)

with open('utils/brick_to_wg_wug.pkl', 'wb') as f:
    pickle.dump(brick_to_wg_wug_translation_table, f)