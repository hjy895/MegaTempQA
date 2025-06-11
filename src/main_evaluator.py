"""
Main script for evaluating models on MegaTempQA
"""

import argparse
from evaluation.evaluator import ModelEvaluator
from utils.config import EvaluationConfig
from utils.logging_utils import setup_logging

def main():
    parser = argparse.ArgumentParser(description='Evaluate Models on MegaTempQA')
    parser.add_argument('--dataset', required=True,
                       help='Path to dataset CSV file')
    parser.add_argument('--output_dir', default='results',
                       help='Output directory for results')
    parser.add_argument('--models', nargs='+',
                       help='Models to evaluate (default: all)')
    parser.add_argument('--sample_size', type=int, default=50,
                       help='Sample size per model')
    parser.add_argument('--max_shots', type=int, default=3,
                       help='Maximum shots to test')
    parser.add_argument('--config', help='Config file path')
    parser.add_argument('--verbose', action='store_true',
                       help='Enable verbose logging')
    
    args = parser.parse_args()
    
    # Setup logging
    setup_logging(verbose=args.verbose)
    
    # Load configuration
    if args.config:
        config = EvaluationConfig.from_file(args.config)
    else:
        config = EvaluationConfig(
            dataset_path=args.dataset,
            output_dir=args.output_dir,
            sample_size=args.sample_size,
            max_shots=args.max_shots,
            models=args.models
        )
    
    # Run evaluation
    evaluator = ModelEvaluator(config)
    results = evaluator.evaluate()
    
    print(f"✅ Evaluation completed! Results saved to {config.output_dir}")

if __name__ == "__main__":
    main()
