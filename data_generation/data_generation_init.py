"""
Data Generation Module

Contains components for generating temporal QA pairs:
- Dataset generator
- Knowledge base
- Question types and templates
- Quality validators
"""

from .generator import DatasetGenerator
from .knowledge_base import KnowledgeBase
from .question_types import QuestionType, TemporalQuestion
from .validators import QuestionValidator

__all__ = [
    'DatasetGenerator',
    'KnowledgeBase', 
    'QuestionType',
    'TemporalQuestion',
    'QuestionValidator'
]
