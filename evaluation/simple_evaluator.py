"""
Main model evaluator for MegaTempQA
"""

import pandas as pd
import numpy as np
from datetime import datetime
from pathlib import Path
import json

from .model_manager import ModelManager
from .metrics import TemporalQAMetrics
from .prompt_builder import PromptBuilder
from .result_analyzer import ResultAnalyzer
from ..utils.config import EvaluationConfig

class ModelEvaluator:
    """Main evaluator for temporal QA models"""
    
    def __init__(self, config: EvaluationConfig):
        self.config = config
        self.output_dir = Path(config.output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        self.model_manager = ModelManager()
        self.metrics = TemporalQAMetrics()
        self.prompt_builder = PromptBuilder()
        self.analyzer = ResultAnalyzer()
        
        print("🚀 MegaTempQA Model Evaluator")
        print(f"📊 Dataset: {config.dataset_path}")
        print(f"🎯 Models: {len(config.models)}")
        print(f"📝 Sample size: {config.sample_size}")
    
    def evaluate(self) -> pd.DataFrame:
        """Run complete evaluation"""
        # Load dataset
        df = self._load_dataset()
        eval_df = self._create_sample(df)
        examples = self._create_examples(df)
        
        print(f"📊 Evaluation sample: {len(eval_df)} questions")
        print(f"📚 Few-shot examples: {len(examples)}")
        
        # Run evaluation for each model
        all_results = []
        
        for model_name in self.config.models:
            print(f"\n🤖 Evaluating {model_name}")
            
            if self.model_manager.load_model(model_name):
                model_results = self._evaluate_model(eval_df, examples, model_name)
                all_results.extend(model_results)
                self.model_manager.unload_model()
            else:
                print(f"❌ Failed to load {model_name}")
        
        # Create results dataframe
        results_df = pd.DataFrame(all_results)
        
        # Analyze and save results
        if not results_df.empty:
            self._save_results(results_df)
            self.analyzer.generate_report(results_df, self.output_dir)
        
        return results_df
    
    def _load_dataset(self) -> pd.DataFrame:
        """Load and prepare dataset"""
        print(f"📊 Loading dataset: {self.config.dataset_path}")
        
        df = pd.read_csv(self.config.dataset_path)
        
        # Basic cleaning
        df = df.dropna(subset=['question', 'answer'])
        df = df[df['question'].str.len() > 10]
        df = df[df['answer'].str.len() > 0]
        
        print(f"✅ Loaded {len(df):,} questions")
        return df
    
    def _create_sample(self, df: pd.DataFrame) -> pd.DataFrame:
        """Create stratified evaluation sample"""
        # Sample by question type for diversity
        question_types = df['question_type'].unique()[:5]  # Top 5 types
        samples_per_type = self.config.sample_size // len(question_types)
        
        eval_samples = []
        for qtype in question_types:
            type_df = df[df['question_type'] == qtype]
            if len(type_df) > 0:
                sample = type_df.sample(
                    n=min(samples_per_type, len(type_df)), 
                    random_state=42
                )
                eval_samples.append(sample)
        
        return pd.concat(eval_samples).reset_index(drop=True)
    
    def _create_examples(self, df: pd.DataFrame) -> list:
        """Create few-shot examples"""
        # High-quality examples for few-shot learning
        examples_df = df.copy()
        
        if 'confidence_score' in df.columns:
            examples_df = examples_df[examples_df['confidence_score'] >= 0.9]
        
        if 'difficulty' in df.columns:
            examples_df = examples_df[examples_df['difficulty'] <= 2]
        
        # Sample diverse examples
        examples = []
        for qtype in df['question_type'].unique()[:5]:
            type_examples = examples_df[examples_df['question_type'] == qtype]
            if len(type_examples) > 0:
                sample = type_examples.sample(n=min(10, len(type_examples)), random_state=42)
                for _, row in sample.iterrows():
                    examples.append({
                        'question': row['question'],
                        'answer': row['answer'],
                        'type': row['question_type']
                    })
        
        return examples[:50]  # Limit total examples
    
    def _evaluate_model(self, eval_df: pd.DataFrame, examples: list, model_name: str) -> list:
        """Evaluate single model"""
        results = []
        
        for shots in range(self.config.max_shots + 1):  # 0 to max_shots
            print(f"  📋 Testing {shots}-shot...")
            
            shot_examples = examples[:shots] if shots > 0 else []
            
            for _, row in eval_df.iterrows():
                try:
                    # Generate prompt
                    prompt = self.prompt_builder.create_prompt(
                        row['question'], shot_examples
                    )
                    
                    # Get prediction
                    prediction = self.model_manager.generate(prompt)
                    
                    # Calculate metrics
                    metrics = self.metrics.calculate_all_metrics(
                        prediction, row['answer']
                    )
                    
                    # Store result
                    result = {
                        'model': model_name,
                        'shots': shots,
                        'question_type': row.get('question_type', 'unknown'),
                        'domain': row.get('domain', 'general'),
                        'question': row['question'],
                        'true_answer': row['answer'],
                        'predicted_answer': prediction,
                        **metrics
                    }
                    results.append(result)
                    
                except Exception as e:
                    print(f"    ⚠️ Error: {e}")
                    continue
            
            # Print shot results
            if results:
                recent_results = [r for r in results if r['shots'] == shots]
                if recent_results:
                    avg_f1 = np.mean([r['f1'] for r in recent_results])
                    print(f"    📊 {shots}-shot F1: {avg_f1:.3f}")
        
        return results
    
    def _save_results(self, results_df: pd.DataFrame):
        """Save evaluation results"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Save detailed results
        results_file = self.output_dir / f"evaluation_results_{timestamp}.csv"
        results_df.to_csv(results_file, index=False)
        
        # Save summary
        summary = {
            'evaluation_date': timestamp,
            'dataset': str(self.config.dataset_path),
            'models_evaluated': list(results_df['model'].unique()),
            'total_predictions': len(results_df),
            'sample_size': self.config.sample_size,
            'config': self.config.__dict__
        }
        
        summary_file = self.output_dir / f"evaluation_summary_{timestamp}.json"
        with open(summary_file, 'w') as f:
            json.dump(summary, f, indent=2)
        
        print(f"💾 Results saved to {results_file}")
        print(f"📊 Summary saved to {summary_file}")
