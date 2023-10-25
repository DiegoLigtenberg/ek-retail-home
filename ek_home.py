#az storage blob download-batch --destination "C:/ek-images" --source ekhome --account-name saekmatilliontest --account-key "x6iqVhYaWfqH4qBwqQ4t0RqhdJb+qimxCImBqTZTdXHZ2m0aS6Q6xNysecUn0ECoUrsEqosSL2i6+AStSXfNxg==" --pattern "images/*"
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

# Directory containing the JPG images  
image_directory = Path('data/Artikelbilder/Bilder_Fissler/')  # Convert the directory path to a Path object
jpg_files = sorted(image_directory.glob("*.jpg")) # List all JPG files in the directory using glob

# load labels german and english(translated)
with open ('utils/labels_list.pkl','rb') as f:
    labels_list = pickle.load(f)
with open ('utils/labels_list_translated.pkl','rb') as f:
    labels_list_translated = pickle.load(f)

# Initialize the start time
start_time = time.time()

# Loop over each JPG image and load using PIL
final_predictions = []
for it ,jpg_file in enumerate(jpg_files):
    image = Image.open(jpg_file)

    kategorie_prediction = []
    for kategorie in range(len(labels_list)):

        candidate_labels_translated = labels_list_translated[kategorie]  # use translated (english) labels for model
        candidate_labels = labels_list[kategorie]  # use raw german labels for output
        inputs = processor(images=image, text=candidate_labels_translated, return_tensors="pt", padding=True)

        with torch.no_grad():
            outputs = model(**inputs)

        logits = outputs.logits_per_image[0]
        probs = logits.softmax(dim=-1).numpy()

        result = [
            {"score": score, "label": candidate_label}
            for score, candidate_label in sorted(zip(probs, candidate_labels_translated), key=lambda x: -x[0])
        ]
        kategorie_prediction.append(result[0]['label'])
    jpg_file = jpg_file.relative_to('data')
    final_predictions.append([jpg_file] + kategorie_prediction)
    print(str(it)+"/"+str(len(jpg_files)),end='\r')
    # break

# Create DataFrame
columns = ['image_file'] + [f'Kategorie {i+1}' for i in range(len(labels_list))]
df = pd.DataFrame(final_predictions, columns=columns)

df.to_excel('test_predictions.xlsx',index=False)

# Calculate the elapsed time
elapsed_time = time.time() - start_time
print(f"Total time taken: {elapsed_time:.2f} seconds")

print("All images processed.")



