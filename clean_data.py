import json
import re

def load_homophones(homophone_file):
    with open(homophone_file, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    homophone_sets = data["homophones"]
    sorted_homophones = {tuple(sorted(set(group))): group for group in homophone_sets}
    return sorted_homophones

def clean_text(text):
    # Remove links
    text = re.sub(r'http\S+', '', text)
    # Remove numbers
    text = re.sub(r'\d+', '', text)
    # Remove English words
    text = re.sub(r'[a-zA-Z]+', '', text)
    # Remove special symbols and unwanted punctuation
    text = re.sub(r'[<>\(\)\!@#\$%\*\)_\+\=\{\}\[\]\|\\/:;"\',.\?~`^&]', '', text)
    # Remove unique Khmer punctuation
    text = re.sub(r'[ៗ។៕៚]', '', text)
    # Remove extra spaces
    text = re.sub(r'\s+', ' ', text).strip()
    
    return text

def structure_cleaned_data(input_file, homophones, output_file):
    with open(input_file, "r", encoding="utf-8") as f:
        structured_data = json.load(f)
    
    cleaned_output = {}
    
    for homophone_set in homophones.keys():  # Follow homophone_test.json order
        for word in homophone_set:
            if word in structured_data:
                cleaned_sentences = [clean_text(sentence) for sentence in structured_data[word] if clean_text(sentence)]
                if cleaned_sentences:  # Ensure we don’t store empty lists
                    cleaned_output[word] = cleaned_sentences
    
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(cleaned_output, f, ensure_ascii=False, indent=4)
    
    print(f"Cleaned structured data saved to {output_file}")

# File paths
homophone_file = "homophone_test.json"
input_file = "structured_output.json"
output_file = "cleaned_output.json"

# Load homophones and clean data
homophones = load_homophones(homophone_file)
structure_cleaned_data(input_file, homophones, output_file)
