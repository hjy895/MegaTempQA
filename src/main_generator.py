"""
Main script for generating the MegaTempQA dataset
"""

import argparse
from pathlib import Path
from data_generation.generator import DatasetGenerator
from utils.config import Config
from utils.logging_utils import setup_logging

def main():
    parser = argparse.ArgumentParser(description='Generate MegaTempQA Dataset')
    parser.add_argument('--output_dir', default='data/generated', 
                       help='Output directory for dataset')
    parser.add_argument('--num_batches', type=int, default=5,
                       help='Number of batches to generate')
    parser.add_argument('--questions_per_batch', type=int, default=50_000_000,
                       help='Questions per batch')
    parser.add_argument('--config', help='Config file path')
    parser.add_argument('--verbose', action='store_true',
                       help='Enable verbose logging')
    
    args = parser.parse_args()
    
    # Setup logging
    setup_logging(verbose=args.verbose)
    
    # Load configuration
    if args.config:
        config = Config.from_file(args.config)
    else:
        config = Config(
            output_dir=args.output_dir,
            num_batches=args.num_batches,
            questions_per_batch=args.questions_per_batch
        )
    
    # Generate dataset
    generator = DatasetGenerator(config)
    generator.generate()
    
    print("✅ Dataset generation completed!")

if __name__ == "__main__":
    main()
