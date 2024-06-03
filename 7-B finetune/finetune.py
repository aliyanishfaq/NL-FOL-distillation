import requests
import json
import time

def post_completion_request(prompt):
    endpoint = 'https://api.together.xyz/v1/completions'
    headers = {
        "Authorization": "Bearer 66f65faccb5114b42f14f8a11a34b05a7f4796f4ba8acb74f16878ff7f1fb024"
    }
    payload = {
        "model": "shreyas3@stanford.edu/CodeLlama-7b-hf-2024-06-03-04-19-11-f996488a",
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
        elif response.status_code == 429:
            print("Rate limit exceeded. Waiting for 1 seconds...")
            time.sleep(1)  # Wait for 1 seconds before retrying
            return post_completion_request(prompt)  # Retry the request
        else:
            raise Exception(f"Failed to generate a rationales with status code {response.status_code}")
    except requests.RequestException as e:
       raise e


#test_dataset_path = '/Users/aliyanishfaq/Documents/GitHub/NL-FOL-distillation/Dataset/Eval/MALLS-v0.1-test.json'
test_dataset_path = '/Users/aliyanishfaq/Documents/GitHub/NL-FOL-distillation/Dataset/Eval/folio_parsed.json'
with open(test_dataset_path, 'r') as f:
    test_data = json.load(f)

output = []

for data in test_data[:500]:
    prompt = f"Translate the following sentence into a first order logic statement: '{data['NL']}'. Only provide the first order logic statement, do not add any other comments or remarks."
    res = post_completion_request(prompt)
    predicted_fol = res
    print('Predicted:', predicted_fol)
    true_fol = data['FOL']
    print('True:', true_fol)
    nl = data['NL']
    output.append({'NL': nl, 'Predicted_FOL': predicted_fol, 'True_FOL': true_fol})

sds_7b_output_filepath = '/Users/aliyanishfaq/Documents/GitHub/NL-FOL-distillation/7-B finetune/sds-7b.json'
with open(sds_7b_output_filepath, 'w') as f:
    json.dump(output, f, indent=4)