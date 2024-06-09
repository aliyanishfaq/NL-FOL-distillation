import json

test_dataset_path = '/Users/aliyanishfaq/Documents/GitHub/NL-FOL-distillation/7-B finetune/sds-7b-34k.json'
with open(test_dataset_path, 'r') as f:
    test_data = json.load(f)

print(len(test_data))