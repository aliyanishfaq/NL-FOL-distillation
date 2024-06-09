import requests
import json
import time
import concurrent.futures

def post_completion_request(prompt, attempt=0):
    endpoint = 'https://api.together.xyz/v1/completions'
    headers = {
        "Authorization": "Bearer 1d3929da2f2264da6d976da8248009a4bd197031ce15dbf52357bd3c6ae03601"
    }
    payload = {
        "model": "aliyan@stanford.edu/CodeLlama-7b-hf-8.1-8.1k-2024-06-08-03-07-59-653346f1",
        "max_tokens": 100,
        "temperature": 0.7,
        "top_p": 0.7,
        "top_k": 50,
        "repetition_penalty": 1,
        "stop": ["</s>"], 
        "messages": [{"content": f"{prompt}", "role": "user"}]
    }
    #return response
    try:
        response = requests.post(endpoint, json=payload, headers=headers)
        if response.status_code == 200:
            response_data = response.json()['choices'][0]['text']
            response_data = response_data.strip()
            return response_data
        elif response.status_code == 429 or response.status_code == 524:
            if attempt <= 5:
                wait_time = 2 ** attempt  # Exponential backoff
                print(f"Request failed with status {response.status_code}. Retrying in {wait_time} seconds...")
                time.sleep(wait_time)
                return post_completion_request(prompt, attempt + 1)
         
        else:
            raise Exception(f"Failed to generate a rationales with status code {response.status_code}. Details {response.text}")
    except requests.RequestException as e:
       raise e


#test_dataset_path = '/Users/aliyanishfaq/Documents/GitHub/NL-FOL-distillation/Dataset/Eval/MALLS-v0.1-test.json'
test_dataset_path = '/Users/aliyanishfaq/Documents/GitHub/NL-FOL-distillation/Dataset/Eval/folio_parsed.json'
with open(test_dataset_path, 'r') as f:
    test_data = json.load(f)

output = []

def process_data(data):
    prompt = f"Translate the following sentence into a first order logic statement: '{data['NL']}'. Only provide the first order logic statement, do not add any other comments or remarks."
    res = post_completion_request(prompt)
    predicted_fol = res
    print('Predicted:', predicted_fol)
    true_fol = data['FOL']
    print('True:', true_fol)
    nl = data['NL']
    return {'NL': nl, 'Predicted_FOL': predicted_fol, 'True_FOL': true_fol}

with concurrent.futures.ThreadPoolExecutor() as executor:
    results = list(executor.map(process_data, test_data))
output.extend(results)

sds_7b_output_filepath = '/Users/aliyanishfaq/Documents/GitHub/NL-FOL-distillation/7-B finetune/sds-7b-8k-7k-2-epoch-chat.json'
with open(sds_7b_output_filepath, 'w') as f:
    json.dump(output, f, indent=4)

'''
for data in test_data:
    prompt = f"Translate the following sentence into a first order logic statement: '{data['NL']}'. Only provide the first order logic statement, do not add any other comments or remarks."
    res = post_completion_request(prompt)
    predicted_fol = res
    print('Predicted:', predicted_fol)
    true_fol = data['FOL']
    print('True:', true_fol)
    nl = data['NL']
    output.append({'NL': nl, 'Predicted_FOL': predicted_fol, 'True_FOL': true_fol})

sds_7b_output_filepath = '/Users/aliyanishfaq/Documents/GitHub/NL-FOL-distillation/7-B finetune/sds-7b-34k-7k-3-epoch.json'
with open(sds_7b_output_filepath, 'w') as f:
    json.dump(output, f, indent=4)
'''