"""
Question type definitions and data structures
"""

from enum import Enum
from dataclasses import dataclass
from typing import Dict, Any

class QuestionType(Enum):
    """All supported temporal question types"""
    ATTRIBUTE_EVENT = "attribute_event"
    ATTRIBUTE_ENTITY = "attribute_entity"
    ATTRIBUTE_TIME = "attribute_time"
    COMPARISON_EVENT = "comparison_event"
    COMPARISON_ENTITY = "comparison_entity"
    COMPARISON_TIME = "comparison_time"
    COUNTING_EVENT = "counting_event"
    COUNTING_ENTITY = "counting_entity"
    CAUSAL_REASONING = "causal_reasoning"
    DURATION_ESTIMATION = "duration_estimation"
    SEQUENCE_ORDERING = "sequence_ordering"
    CROSS_DOMAIN = "cross_domain"
    TEMPORAL_CLUSTERING = "temporal_clustering"
    MULTI_GRANULAR = "multi_granular"
    COUNTERFACTUAL = "counterfactual"
    TEMPORAL_OVERLAP = "temporal_overlap"

class Difficulty(Enum):
    """Question difficulty levels"""
    VERY_EASY = 1
    EASY = 2
    MEDIUM = 3
    HARD = 4
    VERY_HARD = 5

@dataclass
class TemporalQuestion:
    """Data structure for temporal QA pairs"""
    id: str
    question: str
    answer: str
    question_type: str
    difficulty: int
    temporal_granularity: str
    time_span_start: str
    time_span_end: str
    entities_question: str
    countries_question: str
    hop_count: int
    confidence_score: float
    domain: str
    requires_calculation: bool
    complexity_score: float
    source_type: str
    batch_id: int
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for CSV export"""
        return {
            'id': self.id,
            'question': self.question,
            'answer': self.answer,
            'question_type': self.question_type,
            'difficulty': self.difficulty,
            'temporal_granularity': self.temporal_granularity,
            'time_span_start': self.time_span_start,
            'time_span_end': self.time_span_end,
            'entities_question': self.entities_question,
            'countries_question': self.countries_question,
            'hop_count': self.hop_count,
            'confidence_score': self.confidence_score,
            'domain': self.domain,
            'requires_calculation': self.requires_calculation,
            'complexity_score': self.complexity_score,
            'source_type': self.source_type,
            'batch_id': self.batch_id
        }

# Question type metadata
QUESTION_TYPE_INFO = {
    QuestionType.ATTRIBUTE_EVENT: {
        'description': 'Questions about event attributes (when, where, what)',
        'examples': ['When did World War II start?', 'Where did the Moon landing occur?'],
        'difficulty_range': (1, 3),
        'typical_hop_count': 1
    },
    QuestionType.COMPARISON_EVENT: {
        'description': 'Questions comparing two or more events',
        'examples': ['Which happened first: WWI or WWII?', 'Which war had more casualties?'],
        'difficulty_range': (2, 4),
        'typical_hop_count': 2
    },
    QuestionType.CAUSAL_REASONING: {
        'description': 'Questions about cause-effect relationships',
        'examples': ['What caused the Great Depression?', 'How did WWII lead to the Cold War?'],
        'difficulty_range': (4, 5),
        'typical_hop_count': 3
    },
    # Add more as needed...
}
