"""
File utilities for dataset generation and evaluation
"""

import csv
import json
import pandas as pd
from pathlib import Path
from typing import List, Dict, Any

class CSVWriter:
    """Efficient CSV writer for large datasets"""
    
    def __init__(self, filepath: Path):
        self.filepath = filepath
        self.file = None
        self.writer = None
    
    def write_header(self, headers: List[str]):
        """Write CSV header"""
        self.file = open(self.filepath, 'w', encoding='utf-8', newline='')
        self.writer = csv.writer(self.file)
        self.writer.writerow(headers)
    
    def write_batch(self, data: List[Dict[str, Any]]):
        """Write batch of data to CSV"""
        if not data:
            return
        
        if not self.writer:
            raise ValueError("Must call write_header first")
        
        # Get headers from first item
        headers = list(data[0].keys())
        
        for item in data:
            row = [str(item.get(header, '')) for header in headers]
            self.writer.writerow(row)
    
    def close(self):
        """Close file"""
        if self.file:
            self.file.close()

class DataLoader:
    """Efficient data loading utilities"""
    
    @staticmethod
    def load_csv(filepath: str, nrows: int = None) -> pd.DataFrame:
        """Load CSV file with error handling"""
        try:
            df = pd.read_csv(filepath, nrows=nrows)
            return df
        except Exception as e:
            print(f"Error loading CSV {filepath}: {e}")
            return pd.DataFrame()
    
    @staticmethod
    def load_json(filepath: str) -> Dict:
        """Load JSON file with error handling"""
        try:
            with open(filepath, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading JSON {filepath}: {e}")
            return {}
    
    @staticmethod
    def save_json(data: Dict, filepath: str):
        """Save data to JSON file"""
        try:
            with open(filepath, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"Error saving JSON {filepath}: {e}")

class FileValidator:
    """Validate dataset files"""
    
    @staticmethod
    def validate_csv(filepath: str) -> Dict[str, Any]:
        """Validate CSV file and return stats"""
        try:
            df = pd.read_csv(filepath, nrows=1000)  # Sample for validation
            
            stats = {
                'exists': True,
                'readable': True,
                'columns': list(df.columns),
                'sample_rows': len(df),
                'file_size_mb': Path(filepath).stat().st_size / (1024 * 1024)
            }
            
            # Count total rows efficiently
            with open(filepath, 'r') as f:
                total_rows = sum(1 for line in f) - 1  # Subtract header
            stats['total_rows'] = total_rows
            
            return stats
            
        except Exception as e:
            return {
                'exists': Path(filepath).exists(),
                'readable': False,
                'error': str(e)
            }
    
    @staticmethod
    def validate_dataset_batch(directory: str, expected_batches: int) -> Dict:
        """Validate all batch files in directory"""
        results = {
            'total_expected': expected_batches,
            'files_found': 0,
            'total_questions': 0,
            'total_size_mb': 0,
            'batch_results': []
        }
        
        for i in range(1, expected_batches + 1):
            batch_file = Path(directory) / f"batch_{i:03d}.csv"
            
            if batch_file.exists():
                stats = FileValidator.validate_csv(str(batch_file))
                results['files_found'] += 1
                results['total_questions'] += stats.get('total_rows', 0)
                results['total_size_mb'] += stats.get('file_size_mb', 0)
                results['batch_results'].append(stats)
            else:
                results['batch_results'].append({
                    'exists': False,
                    'readable': False,
                    'error': 'File not found'
                })
        
        return results
