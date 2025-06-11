"""
Logging utilities for MegaTempQA
"""

import logging
import sys
from datetime import datetime
from pathlib import Path

def setup_logging(verbose: bool = False, log_file: str = None):
    """Setup logging configuration"""
    
    # Set log level
    level = logging.DEBUG if verbose else logging.INFO
    
    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Setup console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(level)
    console_handler.setFormatter(formatter)
    
    # Setup root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(level)
    root_logger.addHandler(console_handler)
    
    # Setup file handler if specified
    if log_file:
        log_path = Path(log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)
        
        file_handler = logging.FileHandler(log_path)
        file_handler.setLevel(level)
        file_handler.setFormatter(formatter)
        root_logger.addHandler(file_handler)
    
    # Reduce noise from other libraries
    logging.getLogger('transformers').setLevel(logging.WARNING)
    logging.getLogger('torch').setLevel(logging.WARNING)
    logging.getLogger('urllib3').setLevel(logging.WARNING)

class ProgressLogger:
    """Logger for tracking progress"""
    
    def __init__(self, name: str, total: int):
        self.logger = logging.getLogger(name)
        self.total = total
        self.current = 0
        self.start_time = datetime.now()
    
    def update(self, increment: int = 1):
        """Update progress"""
        self.current += increment
        
        if self.current % 1000 == 0:  # Log every 1000 items
            elapsed = datetime.now() - self.start_time
            rate = self.current / elapsed.total_seconds()
            remaining = (self.total - self.current) / rate if rate > 0 else 0
            
            self.logger.info(
                f"Progress: {self.current}/{self.total} "