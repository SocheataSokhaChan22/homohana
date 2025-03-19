import json
import re

# Define the function to clean Khmer text
def clean_khmer_text(text):
    # Remove special characters, numbers, spaces, and emoticons
    text = re.sub(r'[^\u1780-\u17FF]', '', text)
    # Remove English words
    text = re.sub(r'[a-zA-Z]', '', text)
    # Remove Khmer punctuation
    khmer_punctuations = r'[\u17D4\u17D5\u17D6\u17D8\u17DA]'
    text = re.sub(khmer_punctuations, '', text)
    return text

# Load and process the JSONL file
input_path = 'segmentation/dataprocessed/segmented_hellokrupet.jsonl'
output_path = 'segmentation/cleaned_segmented_hellokrupet.jsonl'

cleaned_data = []

with open(input_path, 'r', encoding='utf-8') as f:
    for line in f:
        entry = json.loads(line.strip())  # Parse each line as a JSON object
        # Extract and clean the content and segmented fields
        if 'content' in entry:
            entry['content'] = clean_khmer_text(entry['content'])
        if 'segmented' in entry:
            entry['segmented'] = [clean_khmer_text(segment) for segment in entry['segmented']]
        
        # Remove unwanted fields
        entry.pop('category', None)
        entry.pop('title', None)
        entry.pop('url', None)
        
        cleaned_data.append(entry)

# Save the cleaned data back to a JSONL file
with open(output_path, 'w', encoding='utf-8') as f:
    for cleaned_entry in cleaned_data:
        f.write(json.dumps(cleaned_entry, ensure_ascii=False) + '\n')

print("Data cleaning completed. Cleaned data saved to:", output_path)
