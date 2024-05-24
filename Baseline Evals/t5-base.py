"""
T5-base baseline eval
https://huggingface.co/google-t5/t5-base
"""

from transformers import T5Tokenizer, T5ForConditionalGeneration

model_name = 't5-large'
tokenizer = T5Tokenizer.from_pretrained(model_name, model_max_length=512)
model = T5ForConditionalGeneration.from_pretrained(model_name)

input_text = """translate English to First Order Logic: Every human is mortal.

examples:
"NL": "All people who regularly drink coffee are dependent on caffeine.", "FOL": "\u2200x (Drinks(x) \u2192 Dependent(x))"
"NL": "People either regularly drink coffee or joke about being addicted to caffeine.", "FOL": "\u2200x (Drinks(x) \u2295 Jokes(x))"
"NL": "No one who jokes about being addicted to caffeine is unaware that caffeine is a drug.", "FOL": "\u2200x (Jokes(x) \u2192 \u00acUnaware(x))
"""

input_ids = tokenizer.encode(input_text, return_tensors="pt",  max_length=512, truncation=True)
outputs = model.generate(input_ids)
output_text = tokenizer.decode(outputs[0], skip_special_tokens=True)

print("Generated FOL:", output_text)