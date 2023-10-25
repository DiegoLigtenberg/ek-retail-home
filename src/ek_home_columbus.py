from transformers import AutoProcessor, AutoModelForZeroShotImageClassification
from PIL import Image
import torch
from pathlib import Path
import pandas as pd
import pickle
import time

# Initialize the CLIP model and processor
checkpoint = "openai/clip-vit-large-patch14"
model = AutoModelForZeroShotImageClassification.from_pretrained(checkpoint)
processor = AutoProcessor.from_pretrained(checkpoint)

print('hello world')
import sys
sys.exit()
# Directory containing the JPG images
image_directory = Path('C:/ek-images/Images')
jpg_files = sorted(image_directory.glob("*.jpg"))



# Load labels (translated)
with open('utils/brick_title_list.pkl', 'rb') as f:
    labels_list_translated = pickle.load(f)

# Initialize the start time
start_time = time.time()

batch_size = 64  # Define your batch size

# Initialize lists for images and corresponding labels
images = []
final_predictions = []

# process all images or just a fixed set
jpg_files = jpg_files[::]

for it, jpg_file in enumerate(jpg_files):
    image = Image.open(jpg_file)
    image = image.resize(size=(500, 500), resample=Image.Resampling.BICUBIC)
    images.append(image)

    # Process the batch
    if len(images) == batch_size or it == len(jpg_files) - 1:        
        inputs = processor(images=images, text=labels_list_translated, return_tensors="pt", padding=True)

        with torch.no_grad():
            outputs = model(**inputs)

        logits = outputs.logits_per_image
        probs = logits.softmax(dim=1).numpy()

        # loop again over all the images (because this is batched)
        for i, img_file in enumerate(jpg_files[it - len(images) + 1: it + 1]):
            kategorie_prediction = []
            result = [
                {"score": score, "label": label}
                for score, label in sorted(zip(probs[i], labels_list_translated), key=lambda x: -x[0])
            ]
            kategorie_prediction.append(result[0]['label'])
            final_predictions.append([img_file] + kategorie_prediction)

        # Reset the images next batch
        images = []

    print(f"Batch {it // batch_size + 1}/{1+len(jpg_files) // batch_size} processed", end='\r')

# Create DataFrame
columns = ['image_file'] + ['Kategorie 4']
df = pd.DataFrame(final_predictions, columns=columns)
print(df)

df.to_excel('test_predictions_brick2.xlsx', index=False)

# Calculate the elapsed time
elapsed_time = time.time() - start_time
print(f"Total time taken: {elapsed_time:.2f} seconds")

print("All images processed.")
