import json

def load_homophones(homophone_file):
    with open(homophone_file, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data["homophones"]

def load_cleaned_data(cleaned_file):
    with open(cleaned_file, "r", encoding="utf-8") as f:
        return json.load(f)

def analyze_homophones(homophones, cleaned_data):
    homophone_summary = {}
    missing_homophones = []

    for homophone_set in homophones:
        homophone_key = ", ".join(homophone_set)  # Convert tuple to a string key
        homophone_summary[homophone_key] = {}

        has_sentence = False
        for word in homophone_set:
            if word in cleaned_data:
                sentence_count = len(cleaned_data[word])
                homophone_summary[homophone_key][word] = sentence_count
                has_sentence = True
            else:
                homophone_summary[homophone_key][word] = 0

        if not has_sentence:
            missing_homophones.append(homophone_key)  # Keep track of missing sets

    return homophone_summary, missing_homophones

def save_results(homophone_summary, missing_homophones, output_file):
    results = {
        "homophone_summary": homophone_summary,
        "missing_homophones": missing_homophones
    }
    
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=4)

    print(f"Analysis saved to {output_file}")

# File paths
homophone_file = "homophone_test.json"
cleaned_file = "cleaned_output.json"
output_file = "homophone_analysis.json"

# Load data and analyze
homophones = load_homophones(homophone_file)
cleaned_data = load_cleaned_data(cleaned_file)
homophone_summary, missing_homophones = analyze_homophones(homophones, cleaned_data)

# Save results
save_results(homophone_summary, missing_homophones, output_file)
