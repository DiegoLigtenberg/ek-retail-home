from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
import azure.core.exceptions
import os 
from dotenv import load_dotenv, find_dotenv
from pathlib import Path
import time
from settings import *

load_dotenv(find_dotenv(),override=True) # if dotenv already exists, then overwrite it!

# CONNECTION_STRING = os.getenv("CONNECTION_STRING")
#TODO Check that folder starts with Image/xx.jpg because is_Valid checks for that right now

class AzureConnection:
    """
    This class connects to an Azure Blob Storage container using the provided connection string.
    The connection string is typically obtained from an Azure Storage account's access keys -> connection string.
    
    Args:
        container_name (str): The name of the Azure container to connect to.

    Attributes:
        container_client: The Azure Blob Storage container client.

    Methods:
        list_blobs: List of all blobs (image files) in the connected container (client).
    """

    def __init__(self, container_name):
        self.container_name = container_name
        self.container_client = self._connect_container_client(container_name)

    @classmethod
    def blob_service_client(cls):
        blob_service_client = BlobServiceClient.from_connection_string(CONNECTION_STRING)
        return blob_service_client

    def _connect_container_client(self, container_name):
        
        blob_service_client = BlobServiceClient.from_connection_string(CONNECTION_STRING)
        container_client = blob_service_client.get_container_client(container_name)
        return container_client

    def list_blobs(self):
        try:
            return self.container_client.list_blobs()
        except Exception as e:
            print(f"An error occurred while listing blobs: {e}")
            return []
        
class AzureImageLoader:
    """
    Loads images from an Azure Blob Storage container using an AzureConnection.
    ~10 seconds per 10k images
    ~8 minutes for 500k images
     
    It allows specifying a maximum number of images
    to load, and it ensures that only valid images are included in the loaded list.

    Args:
        azure_connection (AzureConnection): An instance of AzureConnection for connecting to the container.
        max_images (int, optional): The maximum number of images to load (default is 150).

    Methods:
        load_images: Load images from the connected container.
        _is_valid_image: Check if a blob represents a valid image.
    """
    def __init__(self, azure_connection, max_images=150):
        self.azure_connection = azure_connection
        self.max_images = max_images

    def load_images(self):
        img_list = []
        try:
            blob_list = self.azure_connection.list_blobs()
            print(blob_list)
            for blob in blob_list:
                if self._is_valid_image(blob.name):
                    img_list.append(blob)
                    if len(img_list) >= self.max_images:
                        break
        except Exception as e:
            print(f"An error occurred while loading images: {e}")
        return img_list

    def _is_valid_image(self, blob_name):
        return blob_name.startswith('Images/') and blob_name.lower().endswith(('.png', '.jpg'))

class AzureDataLoader:
    """
    This class allows the iteration over batches of images loaded from an Azure Blob
    Storage container using the provided AzureImageLoader. The batch size can be
    specified.

    Args:
        azure_image_loader (AzureImageLoader): An instance of AzureImageLoader (a list of Azure Image blobs) for loading images.
        batch_size (int, optional): The batch size for iterating over images (default is 64).

    Example:
        azure_connection = AzureConnection('ekhome')
        azure_image_loader = AzureImageLoader(azure_connection, max_images=150)
        data_loader = AzureDataLoader(azure_image_loader, batch_size=32)

        for batch in data_loader:
            # Process the batch of images
            pass
    """

    def __init__(self, azure_connection, azure_image_loader, batch_size=64):
        self.blob_service_client = AzureConnection.blob_service_client()
        self.azure_connection = azure_connection
        self.azure_image_loader = azure_image_loader
        self.batch_size = batch_size
        self.img_list = self.azure_image_loader.load_images()
        self.current_index = 0
        self.local_path = self._init_local_path() # the path where images will be downloaded/stored/deleted

    def _init_local_path(self):
        local_path = Path('./data/Images')
        local_path.mkdir(parents=True, exist_ok=True)
        return local_path

    def __iter__(self):
        return self
    
    def __len__(self):
        total_images = len(self.img_list)
        return (total_images + self.batch_size - 1) // self.batch_size  # Calculate the total number of batches

    def __next__(self):
        self.empty_images_in_temp() # this runs one extra time for last iteration, so data is deleted
        if self.current_index >= len(self.img_list):
            raise StopIteration
        batch = self._get_next_batch()
        temp_batch_file_loc = self._download_and_store_images_in_temp(batch)
        # update index so loop stops at end of images
        self.current_index += self.batch_size
        return temp_batch_file_loc

    def _get_next_batch(self):
        remaining_images = len(self.img_list) - self.current_index
        if remaining_images <= self.batch_size:
            return self.img_list[self.current_index:]
        else:
            return self.img_list[self.current_index:self.current_index + self.batch_size]

    def _download_and_store_images_in_temp(self, batch):
        temp_batch_file_loc = []
        for img_blob in batch:
            blob_name = img_blob.name
            local_file_path = self.local_path / Path(blob_name).name            
            self._download_image(blob_name, local_file_path)
            temp_batch_file_loc.append(local_file_path)
        return temp_batch_file_loc

    def _download_image(self, blob_name, local_file_path):
        blob_client = self.blob_service_client.get_blob_client(container=self.azure_connection.container_name, blob=blob_name)
        blob_data = blob_client.download_blob()
        with open(local_file_path, "wb") as local_file:
            local_file.write(blob_data.readall())

    def empty_images_in_temp(self):    
        local_files = list(self.local_path.iterdir())
        for file in local_files:
            if file.is_file():
                file.unlink()        
        pass    

    def upload_csv_to_azure(self,xlsx_file_path,overwrite=True):                                       #containername = ekhome     folder = Images     filename = test_predictions.csv
        xlsx_file_path_name = Path(xlsx_file_path).name
        container = self.azure_connection.container_name
        blob_folder = 'Images_AI_Output' #self.local_path.name
        blob_client = AzureConnection.blob_service_client().get_blob_client(container=container, blob=f"{blob_folder}/{xlsx_file_path_name}")        
        try:
            with open(xlsx_file_path, mode="rb") as data:
                blob_client.upload_blob(data, overwrite=overwrite)
            print(f"Uploaded to Azure Storage as blob:\t{blob_folder}/{xlsx_file_path_name}")
        except Exception as e:
            print(f"The blob '{blob_folder}/{xlsx_file_path_name}' was not uploaded. Reason: {e}")


if __name__ == "__main__":
    azure_connection = AzureConnection('ekhome')
    azure_image_loader = AzureImageLoader(azure_connection, max_images=250)
    data_loader = AzureDataLoader(azure_connection, azure_image_loader, batch_size=64)
    start_time = time.time()

    for batch in data_loader:
        print("Batch size:", len(batch))
        # Process the batch of images
    print("Elapsed time:", time.time() - start_time)


