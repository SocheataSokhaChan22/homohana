import json
import os
from khmernltk import word_tokenize
from khmernltk.utils import constants

# Define paths
homophone_file = "homophonelist.json"
segmented_sentences_file = "segmentation/cleaned_segmented_hellokrupet.jsonl"
output_file = "segmentation/labeled_sentences.jsonl"

# Load homophone list
with open(homophone_file, "r", encoding="utf-8") as f:
    homophones_data = json.load(f)

# Extract homophone sets into a flat set of words (normalized)
homophone_sets = homophones_data["homophones"]
homophone_words = set(word.strip() for group in homophone_sets for word in group)

# Function to check if a segmented sentence contains any homophone words
def contains_homophone(segmented_sentence):
    return any(word.strip() in homophone_words for word in segmented_sentence)

# Process and label sentences
with open(segmented_sentences_file, "r", encoding="utf-8") as infile, \
     open(output_file, "w", encoding="utf-8") as outfile:
    for line in infile:
        sentence_data = json.loads(line.strip())
        original_sentence = sentence_data.get("sentence", "")
        
        # Perform Khmer word segmentation
        segmented_sentence = word_tokenize(original_sentence)
        
        # Ensure segmentation returns a list
        if isinstance(segmented_sentence, str):  
            segmented_sentence = segmented_sentence.split()  

        print(f"Original: {original_sentence}")  # Debugging print
        print(f"Segmented: {segmented_sentence}")  # Debugging print
        
        # Replace the original sentence string with the segmented list
        sentence_data["sentence"] = segmented_sentence
        
        # Determine label based on presence of homophones
        sentence_data["label"] = 1 if contains_homophone(segmented_sentence) else 0
        
        # Write updated data to output file
        json.dump(sentence_data, outfile, ensure_ascii=False)
        outfile.write("\n")

print(f"Labeled sentences saved to {output_file}")
