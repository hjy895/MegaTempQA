"""
Evaluation metrics for temporal QA
"""

import re
from typing import Tuple

class TemporalQAMetrics:
    """Metrics for evaluating temporal QA performance"""
    
    def __init__(self):
        pass
    
    def calculate_all_metrics(self, pred: str, truth: str) -> dict:
        """Calculate all metrics for a prediction"""
        precision, recall, f1 = self.token_metrics(pred, truth)
        em = self.exact_match(pred, truth)
        containment = self.containment_score(pred, truth)
        
        return {
            'precision': precision,
            'recall': recall,
            'f1': f1,
            'exact_match': em,
            'containment': containment
        }
    
    def normalize_answer(self, answer: str) -> str:
        """Normalize answer for comparison"""
        if not answer:
            return ""
        
        answer = str(answer).lower().strip()
        # Remove punctuation and extra spaces
        answer = re.sub(r'[^\w\s\d]', ' ', answer)
        answer = re.sub(r'\s+', ' ', answer).strip()
        
        return answer
    
    def exact_match(self, pred: str, truth: str) -> float:
        """Calculate exact match score"""
        pred_norm = self.normalize_answer(pred)
        truth_norm = self.normalize_answer(truth)
        
        if not truth_norm:
            return 0.0
        
        # Direct match
        if pred_norm == truth_norm:
            return 100.0
        
        # Partial matching for robustness
        if truth_norm in pred_norm or pred_norm in truth_norm:
            return 100.0
        
        # Number matching (important for temporal data)
        pred_nums = re.findall(r'\b\d+\b', pred_norm)
        truth_nums = re.findall(r'\b\d+\b', truth_norm)
        if pred_nums and truth_nums:
            if any(p in truth_nums for p in pred_nums):
                return 100.0
        
        return 0.0
    
    def token_metrics(self, pred: str, truth: str) -> Tuple[float, float, float]:
        """Calculate token-based precision, recall, F1"""
        pred_norm = self.normalize_answer(pred)
        truth_norm = self.normalize_answer(truth)
        
        if not truth_norm:
            return 0.0, 0.0, 0.0
        
        pred_tokens = set(pred_norm.split()) if pred_norm else set()
        truth_tokens = set(truth_norm.split()) if truth_norm else set()
        
        if not truth_tokens:
            return 0.0, 0.0, 0.0
        
        if not pred_tokens:
            return 0.0, 0.0, 0.0
        
        common_tokens = pred_tokens & truth_tokens
        
        precision = len(common_tokens) / len(pred_tokens)
        recall = len(common_tokens) / len(truth_tokens)
        
        if precision + recall == 0:
            f1 = 0.0
        else:
            f1 = 2 * precision * recall / (precision + recall)
        
        # Scale to 0-100
        return precision * 100, recall * 100, f1 * 100
    
    def containment_score(self, pred: str, truth: str) -> float:
        """Calculate containment score"""
        pred_norm = self.normalize_answer(pred)
        truth_norm = self.normalize_answer(truth)
        
        if not truth_norm:
            return 0.0
        
        pred_tokens = set(pred_norm.split()) if pred_norm else set()
        truth_tokens = set(truth_norm.split()) if truth_norm else set()
        
        if not truth_tokens:
            return 0.0
        
        overlap = len(pred_tokens & truth_tokens)
        return (overlap / len(truth_tokens)) * 100
