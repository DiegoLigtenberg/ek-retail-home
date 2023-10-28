import pandas as pd
from transformers import AutoProcessor, AutoModelForZeroShotImageClassification
from PIL import Image
import torch
from pathlib import Path
import pickle
from dataloader import *
from settings import *

GPU_ENABLED = False

# Initialize the CLIP model and processor
checkpoint = "openai/clip-vit-large-patch14"
model = AutoModelForZeroShotImageClassification.from_pretrained(checkpoint)
if GPU_ENABLED: model.to("cuda")
processor = AutoProcessor.from_pretrained(checkpoint)

azure_connection = AzureConnection('ekhome')
azure_image_loader = AzureImageLoader(azure_connection, max_images=12) # 50.000
data_loader = AzureDataLoader(azure_connection, azure_image_loader, batch_size=2) # 512
labels_list_translated = pickle.load(open('utils/brick_title_list.pkl', 'rb'))

with open('utils/brick_title_to_code.pkl', 'rb') as file:
    brick_title_to_code_lookup_table = pickle.load(file)

final_predictions = []
product_ids = []  # Assuming you have a list of product IDs

# Initialize the start time
start_time = time.time()

for b_num, img_batch in enumerate(data_loader):    
    images = []
    for img_file in img_batch:
        image = Image.open(img_file)
        image = image.resize((500, 500), resample=Image.Resampling.BICUBIC)
        images.append(image)

    inputs = processor(images=images, text=labels_list_translated, return_tensors="pt", padding=True)
    if GPU_ENABLED: inputs = {key: value.to("cuda") for key, value in inputs.items()}

    with torch.no_grad():
        outputs = model(**inputs)
    logits = outputs.logits_per_image
    logits = logits.cpu()
    probs = logits.softmax(dim=1).numpy()

    for i, img_file in enumerate(img_batch):
        brick_title_prediction = []
        result = [
            {"score": score, "label": label}
            for score, label in sorted(zip(probs[i], labels_list_translated), key=lambda x: -x[0])
        ]
        brick_title = result[0]['label']
        
        brick_title_prediction.append(brick_title)

        # Now, look up values from the brick_title_to_code_lookup_table and append to the final_predictions
        if brick_title in brick_title_to_code_lookup_table:
            lookup_result = brick_title_to_code_lookup_table[brick_title]

            # Find the codes for the top 4 alternative labels
            alt_labels = [result[n]['label'] for n in range(1,5)] #including 1, exluding N -> 1,2,3,4
            alt_codes = [brick_title_to_code_lookup_table.get(label, {'BrickCode': None})['BrickCode'] for label in alt_labels]

            # Construct row_data in one step
            row_data = [img_file] + [lookup_result.get(key, None) for key in ['SegmentCode', 'SegmentTitle', 
                                                                                'FamilyCode', 'FamilyTitle',
                                                                                'ClassCode', 'ClassTitle', 
                                                                                'BrickCode']] + [brick_title] + [result[0]['score']] 
            # Add AltLabel and AltCode columns
            for n in range(4): #top5-1
                row_data.extend([alt_labels[n], alt_codes[n]])

            # Append the product_id to each row
            row_data = ["Product_ID"] + row_data

            final_predictions.append(row_data)
        else:
            # Handle the case when the brick_title is not found in the brick_title_to_code_lookup_table
            # You can decide what to do in this case, e.g., fill in with default values
            row_data = [img_file] + [None] * 19
            # Append the product_id to each row
            row_data = ["Product_ID"] + row_data

            final_predictions.append(row_data)
        
    print(str(b_num)+"/"+str(len(data_loader)),end='\r')

# Create DataFrame
columns = ['product_id', 'image_file', 'SegmentCode', 'SegmentTitle', 'FamilyCode', 'FamilyTitle', 'ClassCode', 'ClassTitle', 'BrickCode', 'BrickTitle', 'ConfidenceScore', 'AltLabel1', 'AltCode1', 'AltLabel2', 'AltCode2', 'AltLabel3', 'AltCode3', 'AltLabel4', 'AltCode4']
df = pd.DataFrame(final_predictions, columns=columns)


xlsx_file_path = ('output/ai_predictions.xlsx')
df.to_excel(xlsx_file_path, index=False)
data_loader.upload_csv_to_azure(xlsx_file_path)

# Calculate the elapsed time
elapsed_time = time.time() - start_time
print(f"Total time taken: {elapsed_time:.2f} seconds")

print("All images processed.")
