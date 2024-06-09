"""
Evalaution of predicted FOL and true FOL based  on the following metrics:
- BLEU
- Logical Equivalence

Citation: LogicLLaMA
https://github.com/gblackout/LogicLLaMA/blob/main/metrics.py
"""
import evaluate
from fol_parser import VecRuleEvaluator, parse_text_FOL_to_tree, msplit
import json

class Metrics:
    def __init__(self):
        self.bleu = evaluate.load('bleu')
        self.fol_tokenzier = lambda x: msplit(x)[0]
    
    def FOL_BLEU(self, pred_fol, true_fol):
        min_len = min(map(lambda x: len(self.fol_tokenzier(x)), [pred_fol, true_fol]))
        print(self.fol_tokenzier(pred_fol))
        print(self.fol_tokenzier(true_fol))
        result = self.bleu.compute(predictions=[pred_fol], references=[[true_fol]], tokenizer=self.fol_tokenzier, max_order=min(4, min_len))
        return result['bleu']
    def Logical_Equivalence(self, pred_fol, true_fol):
        true_root, pred_root = parse_text_FOL_to_tree(true_fol), parse_text_FOL_to_tree(pred_fol)
        assert true_root is not None, 'failed to parse true FOL: %s' % true_fol
        if pred_root is None:
            return 0., None, None
        
        score, true_inputs, binded_pred_inputs = VecRuleEvaluator.find_best_LE_score(true_root, pred_root, soft_binding=True, greedy_match=True, top_n=1000)
        return score, true_inputs, binded_pred_inputs

metric = Metrics()

def load_data(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

# Load the dataset
data = load_data('/Users/aliyanishfaq/Documents/GitHub/NL-FOL-distillation/7-B finetune/sds-7b.json')


import numpy as np
import matplotlib.pyplot as plt

logical_equivalence_scores = []
bleu_scores = []
print(len(data))
for entry in data:
    pred_fol = entry['Predicted_FOL']
    true_fol = entry['True_FOL']
    le_score, _, _ = metric.Logical_Equivalence(pred_fol, true_fol)
    bleu_score = metric.FOL_BLEU(pred_fol, true_fol)
    logical_equivalence_scores.append(le_score)
    bleu_scores.append(bleu_score)

# Calculate the median of logical equivalence scores
median_le_score = np.median(logical_equivalence_scores)
print(f"Median Logical Equivalence Score: {median_le_score}")
mean_le_score = np.mean(logical_equivalence_scores)
print(f"Mean Logical Equivalence Score: {mean_le_score}")

# Plotting the histogram of logical equivalence scores
plt.hist(logical_equivalence_scores, bins=10, color='blue', alpha=0.7)
plt.title('Distribution of Logical Equivalence Scores')
plt.xlabel('Score')
plt.ylabel('Frequency')
plt.show()

median_bleu_score = np.median(bleu_scores)
print(f"Median BLEU Score: {median_bleu_score}")
mean_bleu_score = np.mean(bleu_scores)
print(f"Mean BLEU Score: {mean_bleu_score}")

# Plotting the histogram of BLEU scores
plt.hist(bleu_scores, bins=10, color='green', alpha=0.7)
plt.title('Distribution of BLEU Scores')
plt.xlabel('Score')
plt.ylabel('Frequency')
plt.show()