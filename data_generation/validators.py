"""
Question quality validators
"""

import re
from .question_types import TemporalQuestion

class QuestionValidator:
    """Validates question quality and correctness"""
    
    def __init__(self, min_confidence=0.7):
        self.min_confidence = min_confidence
    
    def validate(self, question: TemporalQuestion) -> bool:
        """Validate a temporal question"""
        if not question:
            return False
        
        # Basic validation
        if not self._validate_basic_fields(question):
            return False
        
        # Content validation
        if not self._validate_content(question):
            return False
        
        # Quality validation
        if not self._validate_quality(question):
            return False
        
        return True
    
    def _validate_basic_fields(self, question: TemporalQuestion) -> bool:
        """Validate basic required fields"""
        if not question.question or not question.answer:
            return False
        
        if not question.id or not question.question_type:
            return False
        
        if len(question.question) < 10 or len(question.question) > 300:
            return False
        
        if len(question.answer) < 1 or len(question.answer) > 100:
            return False
        
        return True
    
    def _validate_content(self, question: TemporalQuestion) -> bool:
        """Validate question content quality"""
        # Check for placeholders
        placeholders = ['{', '}', 'None', 'N/A', 'null']
        if any(placeholder in question.question for placeholder in placeholders):
            return False
        
        if any(placeholder in question.answer for placeholder in placeholders):
            return False
        
        # Check answer quality
        if question.answer.lower().strip() in ['unknown', 'none', '', '0']:
            return False
        
        # Check question has sufficient words
        if len(question.question.split()) < 5:
            return False
        
        return True
    
    def _validate_quality(self, question: TemporalQuestion) -> bool:
        """Validate question quality metrics"""
        if question.confidence_score < self.min_confidence:
            return False
        
        if question.difficulty < 1 or question.difficulty > 5:
            return False
        
        if question.hop_count < 1 or question.hop_count > 10:
            return False
        
        return True
    
    def _validate_temporal_consistency(self, question: TemporalQuestion) -> bool:
        """Validate temporal consistency"""
        if question.time_span_start and question.time_span_end:
            try:
                start_year = int(question.time_span_start.split('-')[0])
                end_year = int(question.time_span_end.split('-')[0])
                if start_year > end_year:
                    return False
            except:
                return False
        
        return True
    
    def get_validation_errors(self, question: TemporalQuestion) -> list:
        """Get list of validation errors"""
        errors = []
        
        if not question:
            errors.append("Question is None")
            return errors
        
        if not question.question:
            errors.append("Missing question text")
        
        if not question.answer:
            errors.append("Missing answer")
        
        if question.confidence_score < self.min_confidence:
            errors.append(f"Low confidence: {question.confidence_score}")
        
        if len(question.question) < 10:
            errors.append("Question too short")
        
        if len(question.question) > 300:
            errors.append("Question too long")
        
        return errors
