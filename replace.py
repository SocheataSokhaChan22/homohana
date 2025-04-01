import json
import re

# Define the placeholder for unknown tokens
UNK_TOKEN = "[UNK]"

def replace_text(text):
    """ Replaces unwanted characters with [UNK] instead of removing them. """
    text = re.sub(r"http[s]?://\S+", UNK_TOKEN, text)  # Replace URLs
    text = re.sub(r"[a-zA-Z]+", UNK_TOKEN, text)  # Replace English words
    text = re.sub(r"\d+", UNK_TOKEN, text)  # Replace numbers
    text = re.sub(r"[^ក-៿\s]", UNK_TOKEN, text)  # Replace special characters
    text = re.sub(r"[ៗ។៕៚]", UNK_TOKEN, text)  # Replace unique Khmer punctuation
    text = re.sub(r"\s+", " ", text).strip()  # Normalize spaces
    return text

def replace_structure(input_file, output_file):
    """ Reads structured data, replaces unwanted elements with [UNK], and saves the output. """
    with open(input_file, "r", encoding="utf-8") as infile:
        data = json.load(infile)
    
    replaced_data = {}
    
    for homophone, sentences in data.items():
        replaced_sentences = [replace_text(sentence) for sentence in sentences]
        replaced_data[homophone] = replaced_sentences
    
    with open(output_file, "w", encoding="utf-8") as outfile:
        json.dump(replaced_data, outfile, ensure_ascii=False, indent=4)
    
    print(f"Processed data saved to {output_file}")

# File paths
input_file = "structured_output.json"
output_file = "replaced_output.json"

# Run replacement process
replace_structure(input_file, output_file)
