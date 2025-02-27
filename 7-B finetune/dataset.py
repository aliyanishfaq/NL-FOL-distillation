import json
import random

def format_instruction_label(system_prompt, user_message, model_answer):
    instruct_template = f"""<s>[INST] <<SYS>>
{system_prompt}
<</SYS>>

[LABEL] {user_message} [/INST] {model_answer} </s>"""
    return instruct_template

def format_instruction_rationale(system_prompt, user_message, model_answer):
    instruct_template = f"""<s>[INST] <<SYS>>
{system_prompt}
<</SYS>>

[RATIONALE] {user_message} [/INST] {model_answer} </s>"""
    return instruct_template

train_data_path = '/Users/aliyanishfaq/Documents/GitHub/NL-FOL-distillation/Dataset/Train/MALLS-8k.json'
#rationale_dataset = '/Users/aliyanishfaq/Documents/GitHub/NL-FOL-distillation/Dataset/Train/rationale_dataset.json'
#rationale_gold_dataset = '/Users/aliyanishfaq/Documents/GitHub/NL-FOL-distillation/Dataset/Train/rationale_dataset-gold.json'
with open(train_data_path, 'r') as f:
    train_data = json.load(f)
#with open(rationale_dataset, 'r') as f:
#    rationale_data = json.load(f)
#with open(rationale_gold_dataset, 'r') as f:
#    rationale_gold_data = json.load(f)

fine_tune_dataset = '/Users/aliyanishfaq/Documents/GitHub/NL-FOL-distillation/Dataset/Train/fine_tune_dataset-8.1k-0k-rationales.jsonl'
with open(fine_tune_dataset, 'w') as f:
    for data in train_data:
        user_message = f'Translate the following sentence into a first order logic statement: “{data["NL"]}”. Only provide just the first order logic statement, do not add any other comments or remarks.'
        model_answer = data['FOL']
        system_prompt = f'Your task is to convert natural language to first order logic statement. You are only supposed to output first order logic statement.'
        formatted_string = format_instruction_label(system_prompt, user_message, model_answer)
        jsonl_entry = {
            "text": formatted_string
        }
        f.write(json.dumps(jsonl_entry) + '\n')
    '''
    for data in train_data:
        user_message = f'Translate the following sentence into a first order logic statement: “{data["NL"]}”. Provide an explanation of how to arrive at the answer.'
        model_answer = data['Rationals'] + '\n' + '[FOL] ' + data['FOL']
        system_prompt = f'Given a natural language statement, your task is to think step by step, explain your reasoning and produce a first order logic statement for the natural language statement.'
        formatted_string = format_instruction_rationale(system_prompt, user_message, model_answer)
        jsonl_entry = {
            "text": formatted_string
        }
        f.write(json.dumps(jsonl_entry) + '\n')
    for data in rationale_gold_data:
        user_message = f'Translate the following sentence into a first order logic statement: “{data["NL"]}”. Provide an explanation of how to arrive at the answer.'
        model_answer = data['Rationals'] + '\n' + '[FOL] ' + data['FOL']
        system_prompt = f'Given a natural language statement, your task is to think step by step, explain your reasoning and produce a first order logic statement for the natural language statement.'
        formatted_string = format_instruction_rationale(system_prompt, user_message, model_answer)
        jsonl_entry = {
            "text": formatted_string
        }
        f.write(json.dumps(jsonl_entry) + '\n')
    '''
with open(fine_tune_dataset, 'r') as f:
    fine_tune_data = [json.loads(line) for line in f]
