import json
import re
from khmernltk import sentence_tokenize

# Define Khmer sentence separators
SENTENCE_SEPARATOR = ["◌៓", "។", "៕", "៖", "ៗ", "៘", "៙", "៚", "៛", "ៜ", "៝", "?", "!"]
SEPARATOR_PATTERN = f"({'|'.join(re.escape(sep) for sep in SENTENCE_SEPARATOR)})"

# Function to segment text using Khmer sentence separators
def custom_sentence_segment(text):
    sentences = re.split(SEPARATOR_PATTERN, text)
    segmented_sentences = []
    
    for i in range(0, len(sentences) - 1, 2):  # Process in pairs (sentence, separator)
        sentence = sentences[i].strip()
        separator = sentences[i + 1].strip()
        if sentence:
            segmented_sentences.append(sentence + separator)
    
    return segmented_sentences

def segment_sentences(input_file, output_file):
    segmented_data = []
    
    with open(input_file, 'r', encoding='utf-8') as infile:
        for line_number, line in enumerate(infile, start=1):
            try:
                data = json.loads(line.strip())  # Strip and parse JSON
                content = data.get("content", "").strip()
                
                if content:
                    # First, use khmernltk tokenizer
                    nltk_segmented = sentence_tokenize(content)
                    
                    # Then, apply custom sentence segmentation using Khmer punctuation
                    custom_segmented = [s for seg in nltk_segmented for s in custom_sentence_segment(seg)]
                    
                    # Ensure output is a list of segmented sentences
                    data["segmented"] = custom_segmented
                    
                    segmented_data.append(data)
                    
                if line_number % 100 == 0:
                    print(f"Processed {line_number} lines...")

            except json.JSONDecodeError:
                print(f"Warning: Skipping malformed JSON at line {line_number}")

    # Write segmented data to output file
    with open(output_file, 'w', encoding='utf-8') as outfile:
        for item in segmented_data:
            json.dump(item, outfile, ensure_ascii=False)
            outfile.write('\n')

    print(f"✅ Segmentation completed. Output saved to {output_file}")

if __name__ == "__main__":
    input_path = "/Users/socheatasokhachan/Desktop/homohana/segmentation/data/hellokrupet.jsonl"
    output_path = "/Users/socheatasokhachan/Desktop/homohana/segmentation/dataprocessed/segmented_hellokrupet.jsonl"
    
    segment_sentences(input_path, output_path)