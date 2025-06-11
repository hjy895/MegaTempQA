"""
Tests for dataset generation components
"""

import pytest
import tempfile
from pathlib import Path
import pandas as pd

from src.data_generation.generator import DatasetGenerator
from src.data_generation.knowledge_base import KnowledgeBase
from src.data_generation.validators import QuestionValidator
from src.data_generation.question_types import TemporalQuestion, QuestionType
from src.utils.config import Config

class TestKnowledgeBase:
    """Test knowledge base functionality"""
    
    def test_knowledge_base_loading(self):
        """Test knowledge base loads successfully"""
        kb = KnowledgeBase()
        kb.load()
        
        assert len(kb.events) > 0
        assert len(kb.people) > 0
        assert len(kb.organizations) > 0
    
    def test_knowledge_base_stats(self):
        """Test knowledge base statistics"""
        kb = KnowledgeBase()
        kb.load()
        
        stats = kb.get_stats()
        assert 'events' in stats
        assert 'people' in stats
        assert 'organizations' in stats
        assert all(count > 0 for count in stats.values())

class TestQuestionValidator:
    """Test question validation"""
    
    def test_valid_question(self):
        """Test validation of valid question"""
        validator = QuestionValidator()
        
        question = TemporalQuestion(
            id="test_001",
            question="When did World War II begin?",
            answer="1939",
            question_type=QuestionType.ATTRIBUTE_EVENT.value,
            difficulty=2,
            temporal_granularity="year",
            time_span_start="1900-01-01",
            time_span_end="2000-12-31",
            entities_question='["World War II"]',
            countries_question='["Global"]',
            hop_count=1,
            confidence_score=0.95,
            domain="military",
            requires_calculation=False,
            complexity_score=0.3,
            source_type="curated",
            batch_id=1
        )
        
        assert validator.validate(question) == True
    
    def test_invalid_question_empty(self):
        """Test validation of invalid question with empty fields"""
        validator = QuestionValidator()
        
        question = TemporalQuestion(
            id="test_002",
            question="",  # Empty question
            answer="1939",
            question_type=QuestionType.ATTRIBUTE_EVENT.value,
            difficulty=2,
            temporal_granularity="year",
            time_span_start="1900-01-01",
            time_span_end="2000-12-31",
            entities_question='[]',
            countries_question='[]',
            hop_count=1,
            confidence_score=0.95,
            domain="military",
            requires_calculation=False,
            complexity_score=0.3,
            source_type="curated",
            batch_id=1
        )
        
        assert validator.validate(question) == False
    
    def test_low_confidence_question(self):
        """Test validation of low confidence question"""
        validator = QuestionValidator(min_confidence=0.8)
        
        question = TemporalQuestion(
            id="test_003",
            question="When did something happen?",
            answer="sometime",
            question_type=QuestionType.ATTRIBUTE_EVENT.value,
            difficulty=2,
            temporal_granularity="year",
            time_span_start="1900-01-01",
            time_span_end="2000-12-31",
            entities_question='[]',
            countries_question='[]',
            hop_count=1,
            confidence_score=0.5,  # Low confidence
            domain="general",
            requires_calculation=False,
            complexity_score=0.3,
            source_type="curated",
            batch_id=1
        )
        
        assert validator.validate(question) == False

class TestDatasetGenerator:
    """Test dataset generation"""
    
    def test_generator_initialization(self):
        """Test generator initializes correctly"""
        with tempfile.TemporaryDirectory() as temp_dir:
            config = Config(
                output_dir=temp_dir,
                num_batches=1,
                questions_per_batch=100
            )
            
            generator = DatasetGenerator(config)
            assert generator.config.total_questions == 100
            assert Path(temp_dir).exists()
    
    def test_small_generation(self):
        """Test generation of small dataset"""
        with tempfile.TemporaryDirectory() as temp_dir:
            config = Config(
                output_dir=temp_dir,
                num_batches=1,
                questions_per_batch=10
            )
            
            generator = DatasetGenerator(config)
            generator.generate()
            
            # Check output files exist
            batch_file = Path(temp_dir) / "batch_001.csv"
            summary_file = Path(temp_dir) / "dataset_summary.json"
            
            assert batch_file.exists()
            assert summary_file.exists()
            
            # Check batch file has content
            df = pd.read_csv(batch_file)
            assert len(df) > 0
            assert 'question' in df.columns
            assert 'answer' in df.columns

if __name__ == "__main__":
    pytest.main([__file__])
