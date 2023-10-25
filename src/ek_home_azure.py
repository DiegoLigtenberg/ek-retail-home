from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
import azure.core.exceptions
import os 
from dotenv import load_dotenv, find_dotenv, dotenv_values
from pathlib import Path

load_dotenv(find_dotenv(),override=True) # if dotenv already exists, then overwrite it!
CONNECTION_STRING = os.getenv("CONNECTION_STRING")
blob_service_client = BlobServiceClient.from_connection_string(CONNECTION_STRING)

# Set up local file and container
local_path = "./data"
if not os.path.exists(local_path): os.mkdir(local_path)
container_name = 'ekhome'

# Create or reuse the container based on the (already existing) container variable
container_client = blob_service_client.get_container_client(container_name)

img_list = []
# List the blobs in the container
try:
    blob_list = container_client.list_blobs() 
    
    for i,blob in enumerate(blob_list):
        blob_name = blob.name
        if blob_name.startswith('Columbus_Veldes/'):
            if blob_name.lower().endswith('.csv'):
                # Perform actions for CSV files in the 'Columbus_Veldes' folder
                pass
            else:
                # Handle other file types in the 'Columbus_Veldes' folder
                pass
        elif blob_name.startswith('Images/'):
            if blob_name.lower().endswith(('.png', '.jpg')):
                # Perform actions for PNG and JPG files in the 'Images' folder
                img_list.append(blob)


                print(f"Processing PNG/JPG file: {blob_name}")
            else:
                # Handle other file types in the 'Images' folder
                pass

        elif blob_name.startswith('Product_documents/'):
            # Ignore files in the 'Product_documents' folder
            pass
        else:
            # Handle other files in the container
            pass
        if i>200:
            break
except Exception as e:
    print(f"An error occurred while listing blobs: {e}")


# asd

# Download the blob to a local file
# Add 'DOWNLOAD' before the .txt extension so you can see both files in the data directory

# . means 1 subfolder back
local_path = "./data/Images/"
if not os.path.exists(local_path): os.mkdir(local_path)
for blob in img_list:
    blob_name = blob.name
    # preserve the folder structure as it is in azure.
    local_file_path = os.path.join(local_path,os.path.basename(blob_name))

    with open(local_file_path, "wb") as local_file:
        blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)
        blob_data = blob_client.download_blob()
        local_file.write(blob_data.readall())

    print(f"Downloaded: {blob_name}")
    # blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)
asd
    

download_file_path = os.path.join(local_path, str.replace(local_file_name ,'.txt', 'DOWNLOAD.txt'))


container_client = blob_service_client.get_container_client(container= container_name) 
print("\nDownloading blob to \n\t" + download_file_path)
print(download_file_path)
# asd
with open(file=download_file_path, mode="wb") as download_file:
 download_file.write(container_client.download_blob(blob.name).readall())

print("Upload completed.")
asd
# asd

# List the blobs in the container
blob_list = container_client.list_blobs()
for blob in blob_list:
    print("\t" + blob.name + " w00000000000000000000000t")
asd


container_name = "ekhome"  # Your container name
folder_name = "Images"  # Folder within the container
download_count = 10  # Number of images to download



# Create a ContainerClient for the specified container
container_client = blob_service_client.get_container_client(container_name)

# List all blobs in the specified folder
blobs_in_folder = container_client.walk_blobs(folder_name)
downloaded_count = 0

for blob in blobs_in_folder:
    if downloaded_count >= download_count:
        break  # Stop downloading once you reach the desired count
    blob_name = blob.name
    local_path = os.path.join(folder_name, blob_name)
    local_path = blob_name
    # print(blob_name)
    # print(local_path)
   
   

    # Download the blob to a local file
    blob_client = container_client.get_blob_client(blob_name)
    
    with open(r'F:\erik_test', "wb") as f:
        data = blob_client.download_blob()
        data.readinto(f)
