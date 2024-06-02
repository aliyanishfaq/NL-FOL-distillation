import requests
import random
import json


OPENAI_API_URL = "https://api.openai.com/v1/chat/completions"
OPENAI_API_KEY = 'sk-proj-VWiBWvD9WddlgUhg28C5T3BlbkFJ7GpYBfEJjoToA7wNHROa'


def get_rationales(nl, fol):
    messages = [
        {"role": "user", "content": f"""
            Here is a natural language statement: {nl}
         
            Here is its first order logic translation: {fol} 

            Your task is to write a brief explanation to teach how to come up with the first order logic (FOL) statement when given the natural language (NL) statement. Be brief. Actually explain how or why the logic works, why those specific logical operators were chosen (including operators like not, implication, exclusive or, etc.), how to identify what are the predicates and its arguments, how to decide what the quantifiers are, etc. Explain the reasoning behind these choices, don't just state them. When explaining the reasoning, quote evidence for the reasoning directly from the natural language statement. REFERENCING THE NATURAL LANGUAGE STATEMENT WHEN EXPLAINING IS VERY VERY VERY IMPORTANT.

            Strictly follow the same format exactly. Provide the explanation in a similar way with references from the natural language statement. Only output the explanation, nothing else, no other comment or remarks, and no other headings. Nothing except the 3 points in the explanation. DO NOT INCLUDE the title "Explanation". 

            EXAMPLE 

            NL: A vending machine dispenses items such as snacks or beverages in exchange for payment, often in the form of coins or bills. 

            FOL: ∀x ∃y ∃z (VendingMachine(x) ∧ Item(y) ∧ Payment(z) → (Dispenses(x, y) ∧ InExchangeFor(x, z) ∧ (AcceptsCoins(x) ∨ AcceptsBills(x)))) 

            Explanation: 
            - Identify Key Entities and Relationships: The key entities are VendingMachine, Item, and Payment (with subtypes Coin and Bill), and the relationships are Dispenses (VendingMachine, Item), InExchangeFor (Item, Payment), AcceptsCoins (VendingMachine), and AcceptsBills (VendingMachine). Use variables \( x \) for VendingMachine, \( y \) for Item, and \( z \) for Payment.
            - Logical Formulation Structure: Formulate the logic: \( \forall x \exists y \exists z \) (VendingMachine(x) \( \land \) Item(y) \( \land \) Payment(z) \( \rightarrow \) (Dispenses(x, y) \( \land \) InExchangeFor(x, z) \( \land \) (AcceptsCoins(x) \( \lor \) AcceptsBills(x))).
            - Explanation for Logical Formulation: The universal quantifier \( \forall x \) ensures the statement applies to all vending machines ("A vending machine"). Existential quantifiers \( \exists y \) and \( \exists z \) indicate there exists an item and a payment. The predicates VendingMachine(x), Item(y), and Payment(z) identify the vending machine, item, and payment respectively. Dispenses(x, y) and InExchangeFor(x, z) describe the relationships of dispensing items and receiving payments. The disjunction (\( \lor \)) in \( (AcceptsCoins(x) \lor AcceptsBills(x)) \) specifies that the vending machine can accept either coins or bills, capturing the condition "often in the form of coins or bills". Logical conjunctions (\( \land \)) link conditions ("dispenses items...in exchange for payment").
            """}
    ]
    payload = {
        "model": "gpt-4o",
        "messages": messages
    }
    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}"
    }
    try:
        response = requests.post(OPENAI_API_URL, json=payload, headers=headers)
        if response.status_code == 200:
            response_data = response.json()
            generated_text = response_data['choices'][0]['message']['content'] if response_data.get('choices') else ""
            if generated_text.strip():  # Check if the response has content
                return generated_text
            # else continue to the next iteration for retrying
        else:
            raise Exception(f"Failed to generate a rationales with status code {response.status_code}")
    except requests.RequestException as e:
       raise e
    
train_data_path = '/Users/aliyanishfaq/Documents/GitHub/NL-FOL-distillation/Dataset/Train/MALLS-v0.1-train.json'
with open(train_data_path, 'r') as f:
    train_data = json.load(f)

sample_size = int(len(train_data) * 0.2)
selected_entries = random.sample(train_data, sample_size)

results = []
for entry in selected_entries:
    nl = entry['NL']
    fol = entry['FOL']
    rationals = get_rationales(nl, fol)
    if rationals:
        results.append({'NL': nl, 'FOL': fol, 'Rationals': rationals})
    else:
        print("Failed to generate rationales for ", nl)
        break

# Write the results to a new JSON file
rationale_tune_dataset = '/Users/aliyanishfaq/Documents/GitHub/NL-FOL-distillation/Dataset/Train/rationale_dataset.json'
with open(rationale_tune_dataset, 'w') as outfile:
    json.dump(results, outfile, indent=4)

print(results)
