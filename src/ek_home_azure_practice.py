from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
import azure.core.exceptions
import os 
from dotenv import load_dotenv, find_dotenv, dotenv_values

# load_dotenv() # this also works
# load_dotenv(find_dotenv()) 
load_dotenv(find_dotenv(),override=True) # if dotenv already exists, then overwrite it!

CONNECTION_STRING = os.getenv("CONNECTION_STRING") # this is a connection string for a given container

# Configuration - Set these variables to control overwriting
OVERWRITE_CONTAINER = True  # Set to True to overwrite the container, or False to not overwrite
OVERWRITE_FILES = True      # Set to True to overwrite files, or False to not overwrite
blob_service_client = BlobServiceClient.from_connection_string(CONNECTION_STRING)

# Set up local file and container
local_path = "./data/folder1/"
if not os.path.exists(local_path): os.mkdir(local_path)
local_file_name = "mytestfile.txt"
upload_file_path = os.path.join(local_path, local_file_name)
container_name = 'pythoncontainer'
blob_folder = 'folder1'  # Specify the folder name

# Write text to the local file
with open(upload_file_path, mode='w') as file:
    file.write("Hello, World!")

# Create or reuse the container based on the OVERWRITE_CONTAINER variable
container_client = blob_service_client.get_container_client(container_name)

# if OVERWRITE_CONTAINER:
#     try:
#         container_client.create_container()
#     except azure.core.exceptions.ResourceExistsError:
#         print(f"The container '{container_name}' already exists. Using the existing container.")

# Upload the local file with the folder structure # can specify folder_name and file_name separately
blob_client = blob_service_client.get_blob_client(container=container_name, blob=f"{blob_folder}/{local_file_name}")
print(f"Uploading to Azure Storage as blob:\t{blob_folder}/{local_file_name}")

try:
    with open(upload_file_path, mode="rb") as data:
        blob_client.upload_blob(data, overwrite=OVERWRITE_FILES)
except azure.core.exceptions.ResourceExistsError:
    print(f"The blob '{blob_folder}/{local_file_name}' already exists. It has been overwritten.")

asd
# List the blobs in the container
try:
    blob_list = container_client.list_blobs() 
    print(blob_list, "w00t")
    for blob in blob_list:
        print(blob.name)
except Exception as e:
    print(f"An error occurred while listing blobs: {e}")
asd

# Download the blob to a local file
# Add 'DOWNLOAD' before the .txt extension so you can see both files in the data directory
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
