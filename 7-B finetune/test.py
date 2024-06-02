import json

rationale_tune_dataset = '/Users/aliyanishfaq/Documents/GitHub/NL-FOL-distillation/Dataset/Train/rationale_dataset.json'
with open(rationale_tune_dataset, 'r') as f:
    rationale_data = json.load(f)

print(len(rationale_data))