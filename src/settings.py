import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv(),override=True)

CONNECTION_STRING = os.getenv("CONNECTION_STRING")
BATCH_SIZE = 64

