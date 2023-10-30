

import snowflake.connector
from snowflake.connector import SnowflakeConnection
from snowflake.connector import pandas_tools
import pandas as pd
# from model import Img2Table   

INPUT_DIR = 'dataset/suppliers'
TABLE_NAME = 'EK_FASHION_COMPUTER_VISION_TABLE_DEV'


conn = SnowflakeConnection(
    
    account='wc19998.west-europe.azure',
    user='APP_MATILLION_FASHION_DEV',
    password='Z2EcG57cjr8vvrn5LdCcjJ9s',
    role='ROLE_MATILLION_FASHION_DEV',    
    warehouse='DEV_COMPUTE_FASHION',
    database='FASHION_DEV',    
    schema='EK_FASHION_COMPUTER_VISION_SCHEMA',
)
cursor = conn.cursor()

asd

img2table = Img2Table(INPUT_DIR)

# override input dir with dataframe
df_input = pd.read_csv('final_preprocessed_train_dataset.csv')['image_dir']
#error images test
#df_input = [r'F:/GitHub/ek-retail_image_classification/dataset/new_data/4251238948244_2.jpg','F:/GitHub/ek-retail_image_classification/dataset/new_data/4251238888335_1.jpg']

img2table._image_paths = df_input

df = img2table.generate_result()
df.to_csv('ek_retail_datset_suppliers.csv',index=False)

# Remove the last column from the DataFrame
# df = df.iloc[:, :-1]

# columns need to be uppercased, otherwise it doesn't work because snowflake is case sensitive
df.columns = [c.upper() for c in df.columns] 

# Drop the table if it already exists
drop_table_query = "DROP TABLE IF EXISTS {table_name}".format(table_name=TABLE_NAME)
cursor.execute(drop_table_query)

create_table_query = '''
CREATE TABLE IF NOT EXISTS {table_placeholder} (
    IMAGE_DIR STRING,
    MODEL_PREDICTION_1 STRING,
    MODEL_PREDICTION_1_VALUE FLOAT,
    MODEL_PREDICTION_2 STRING,
    MODEL_PREDICTION_2_VALUE FLOAT,
    MODEL_PREDICTION_3 STRING,
    MODEL_PREDICTION_3_VALUE FLOAT,
    MODEL_PREDICTION_COLOR_NAME STRING,
    MODEL_PREDICTION_COLOR_CODE FLOAT,
    MODEL_PREDICTION_COLOR_VALUE FLOAT
)
'''
formatted_query = create_table_query.format(table_placeholder=TABLE_NAME)

cursor.execute(formatted_query)

# Export the DataFrame to Snowflake
pandas_tools.write_pandas(conn, df, 'EK_FASHION_COMPUTER_VISION_TABLE_DEV')

cursor.close()
conn.close()