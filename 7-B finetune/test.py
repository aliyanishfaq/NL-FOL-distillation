import json

test_dataset_path = '/Users/aliyanishfaq/Documents/GitHub/NL-FOL-distillation/Dataset/Eval/MALLS-v0.1-test.json'
with open(test_dataset_path, 'r') as f:
    test_data = json.load(f)

print(len(test_data))