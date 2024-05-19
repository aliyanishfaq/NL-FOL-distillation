"""
Evalaution of predicted FOL and true FOL based  on the following metrics:
- BLEU
- Logical Equivalence

Citation: LogicLLaMA
https://github.com/gblackout/LogicLLaMA/blob/main/metrics.py
"""
import evaluate
from fol_parser import VecRuleEvaluator, parse_text_FOL_to_tree, msplit

class Metrics:
    def __init__(self):
        self.bleu = evaluate.load('bleu')
        self.fol_tokenzier = lambda x: msplit(x)[0]
    
    def FOL_BLEU(self, pred_fol, true_fol):
        min_len = min(map(lambda x: len(self.fol_tokenzier(x)), [pred_fol, true_fol]))
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

true_fol = """
∃x (Film(x) ∧ ((Drama(x) ∧ LongRuntime(x) ∧ MultipleAwards(x)) ∨ (Comedy(x) ∧ ShorterRuntime(x) ∧ BoxOfficeSuccess(x))))
"""

pred_fol = """
∃x (Film(x) ∧ ((Drama(x) ∧ LongRuntime(x) ∧ MultipleAwards(x)) ∨ (Comedy(x) ∧ ShorterRuntime(x) ∧ BoxOfficeSuccess(x))))
"""

print(metric.FOL_BLEU(pred_fol, true_fol))
print(metric.Logical_Equivalence(pred_fol, true_fol))

