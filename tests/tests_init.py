"""
Test Suite for MegaTempQA

Contains unit tests and integration tests for:
- Dataset generation components
- Evaluation framework
- Utility functions
- End-to-end workflows
"""

# Test configuration
import pytest

# Make sure tests can import from src
import sys
from pathlib import Path

# Add src to Python path for tests
src_path = Path(__file__).parent.parent / "src"
if str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))
