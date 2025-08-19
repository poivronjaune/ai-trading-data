"""
gitdata - A lightweight Python package for fetching and consolidating 
CSV data from public GitHub repositories by ticker symbols.
"""

__version__ = "1.0.0"
__author__ = "GitData Team"

from .fetch import GitHubFetcher
from .process import DataProcessor
from .cli import main

__all__ = ["GitHubFetcher", "DataProcessor", "main"]
