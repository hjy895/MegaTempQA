"""
Configuration classes for MegaTempQA
"""

import json
from dataclasses import dataclass
from typing import List, Optional
from pathlib import Path

@dataclass
class Config:
    """Main configuration for dataset generation"""
    output_dir: str = "data/generated"
    num_batches: int = 5
    questions_per_batch: int = 50_000_000
    start_year: int = 1800
    end_year: int = 2025
    batch_write_size: int = 100_000
    quality_threshold: float = 0.8
    diversity_factor: float = 0.9
    
    @property
    def total_questions(self) -> int:
        return self.num_batches * self.questions_per_batch
    
    @classmethod
    def from_file(cls, filepath: str) -> 'Config':
        """Load config from JSON file"""
        with open(filepath) as f:
            data = json.load(f)
        return cls(**data)
    
    def save(self, filepath: str):
        """Save config to JSON file"""
        with open(filepath, 'w') as f:
            json.dump(self.__dict__, f, indent=2)

@dataclass
class EvaluationConfig:
    """Configuration for model evaluation"""
    dataset_path: str
    output_dir: str = "results"
    sample_size: int = 50
    max_shots: int = 3
    models: Optional[List[str]] = None
    max_new_tokens: int = 30
    temperature: float = 0.3
    batch_size: int = 10
    
    def __post_init__(self):
        if self.models is None:
            self.models = self._get_default_models()
    
    def _get_default_models(self) -> List[str]:
        """Get default model list"""
        return [
            'distilgpt2',
            'microsoft/DialoGPT-medium',
            'google/flan-t5-base',
            'facebook/opt-350m',
            'microsoft/phi-2'
        ]
    
    @classmethod
    def from_file(cls, filepath: str) -> 'EvaluationConfig':
        """Load config from JSON file"""
        with open(filepath) as f:
            data = json.load(f)
        return cls(**data)
    
    def save(self, filepath: str):
        """Save config to JSON file"""
        with open(filepath, 'w') as f:
            json.dump(self.__dict__, f, indent=2)
