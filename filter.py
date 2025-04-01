import json
import re
import os

# Load homophone words from homophonelist.json
def load_homophones(homophone_file):
    with open(homophone_file, "r", encoding="utf-8") as f:
        data = json.load(f)
        homophones = set(word for group in data["homophones"] for word in group)
    return homophones

# Extract sentences that contain exactly one homophone and structure by homophone
def filter_sentences(dataset_folder, homophones, output_file):
    # Dictionary to store homophone sentences
    homophone_sentences = {homophone: [] for homophone in homophones}

    for filename in os.listdir(dataset_folder):
        if filename.endswith(".jsonl"):
            input_file = os.path.join(dataset_folder, filename)
            with open(input_file, "r", encoding="utf-8") as infile:
                for line in infile:
                    data = json.loads(line)  # Load JSON line
                    content = data.get("content", "")  # Get the "content" field

                    # If content is a list, join it into a single string
                    if isinstance(content, list):
                        content = " ".join(content)

                    # Split content into sentences
                    sentences = re.split(r"(?<=[।!?])\s*", content)  

                    for sentence in sentences:
                        words = set(sentence.split())  # Convert sentence to a set of words
                        homophones_in_sentence = words & homophones  # Check if sentence contains any homophones

                        # If there's exactly one homophone in the sentence, categorize it
                        if len(homophones_in_sentence) == 1:
                            homophone = homophones_in_sentence.pop()  # Get the single homophone
                            # Append the sentence under the homophone
                            homophone_sentences[homophone].append(sentence.strip())

    # Save the result as a JSON file with homophone categorization
    with open(output_file, "w", encoding="utf-8") as outfile:
        json.dump(homophone_sentences, outfile, ensure_ascii=False, indent=4)

# File paths
homophone_file = "homophone_test.json"
dataset_folder = "dataset"
output_file = "structured_output.json"

# Load homophones and filter sentences
homophones = load_homophones(homophone_file)
filter_sentences(dataset_folder, homophones, output_file)

print(f"Filtered sentences saved to {output_file}")
