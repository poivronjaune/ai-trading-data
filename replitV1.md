# Overview

GitData is a lightweight Python package designed to fetch, clean, and consolidate financial OHLCV (Open, High, Low, Close, Volume) data from public GitHub repositories. The package provides a simple console interface where users can specify a GitHub username and repository name to download CSV files containing price data. It processes the data by cleaning, deduplicating, and organizing it by ticker symbols into separate CSV files.

**Status**: Complete and fully functional implementation matching PRD requirements.
**Last Updated**: August 17, 2025

## Implementation Summary

The package has been successfully implemented with all PRD requirements:
- ✅ Console interface with Click framework
- ✅ GitHub API integration for CSV file fetching
- ✅ Data cleaning and OHLCV validation
- ✅ Deduplication by datetime index
- ✅ Ticker-based file consolidation
- ✅ Comprehensive error handling
- ✅ Memory-efficient file processing
- ✅ Interactive prompts for user input
- ✅ Progress reporting with emoji indicators

# User Preferences

Preferred communication style: Simple, everyday language.

# System Architecture

## Core Components

The system follows a modular architecture with three main components:

### CLI Module (`cli.py`)
- **Purpose**: Provides a command-line interface using the Click framework
- **Functionality**: Handles user input for GitHub username, repository name, branch selection, and save directory
- **Design Pattern**: Command-line application with interactive prompts
- **Entry Point**: Configured via setuptools to provide `gitdata` console command

### Fetcher Module (`fetch.py`)
- **Purpose**: Handles all GitHub API interactions for downloading CSV files
- **Architecture**: RESTful API client using requests library
- **Rate Limiting**: Implements user agent headers to avoid GitHub API rate limiting
- **Error Handling**: Comprehensive validation for repository accessibility and file downloads
- **Memory Management**: Processes files one by one to handle large repositories efficiently

### Processor Module (`process.py`)
- **Purpose**: Cleans, validates, and consolidates financial data
- **Data Pipeline**: 
  1. Downloads CSV content from GitHub
  2. Validates required OHLCV columns (datetime, open, high, low, close, volume)
  3. Handles multiple ticker column naming conventions
  4. Removes duplicate datetime entries
  5. Groups data by ticker symbol
  6. Saves consolidated data as separate CSV files
- **Data Validation**: Flexible column mapping for different CSV formats
- **Deduplication Strategy**: Keeps first occurrence of duplicate timestamps

## Package Structure

The package uses a standard Python package layout with:
- Setuptools configuration for distribution (setup.py only - removed conflicting pyproject.toml)
- Entry points for console commands  
- Modular design for maintainability
- Version management and metadata

## Data Processing Pipeline

1. **Input Validation**: Validates GitHub repository accessibility
2. **File Discovery**: Recursively finds all CSV files in repository
3. **Content Download**: Downloads file content via GitHub API
4. **Data Cleaning**: Standardizes datetime formats and removes duplicates  
5. **Data Consolidation**: Groups by ticker and saves separate files
6. **Output Generation**: Creates organized CSV files in specified directory

# External Dependencies

## Core Dependencies
- **pandas (>=1.3.0)**: Data manipulation and CSV processing
- **requests (>=2.25.0)**: HTTP client for GitHub API interactions
- **click (>=8.0.0)**: Command-line interface framework

## External APIs
- **GitHub API**: RESTful API for accessing public repository contents
  - No authentication required for public repositories
  - Content API for downloading file contents
  - Tree API for repository structure traversal

## Python Requirements
- **Python 3.10+**: Minimum Python version requirement
- **Standard Library**: Uses os, base64, time, warnings, typing modules

## Data Sources
- **GitHub Repositories**: Public repositories containing CSV files with financial OHLCV data
- **CSV Format Expectations**: Files should contain datetime, OHLCV columns, and ticker/symbol identifiers