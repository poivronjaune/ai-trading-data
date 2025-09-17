# GitData

A lightweight Python package designed to fetch and consolidate CSV data from public GitHub repositories by ticker symbols.
> [!WARNING]
> This code **DOES NOT USE** Ai models when run. The code was generated using vibecoding techniques. 
> 
## Overview

`gitdata` provides a simple console interface where users can specify a GitHub username and repository name containing CSV files. The package downloads and consolidates data by ticker symbols without any modifications to preserve the original data structure.

## Features

- **Simple Console Interface**: Interactive prompts for GitHub username and repository
- **Data Download**: Fetch CSV files from public GitHub repositories using the GitHub API
- **Data Processing**: Raw data consolidation without modification
- **Data Consolidation**: Group by ticker symbol and save as separate CSV files
- **Minimal Processing**: Preserves original data structure and content
- **Error Handling**: Comprehensive error handling for invalid repos and malformed data
- **Memory Efficient**: Process files one by one to handle large repositories

## Installation

```bash
pip install .
```

Or for development:

```bash
pip install -e .
```

The package uses modern Python packaging with `pyproject.toml` configuration.

## Usage

### Command Line Interface

After installation, you can use the `gitdata` command:

```bash
gitdata
```

Or run it directly with Python:

```bash
python -m gitdata.cli
```

### Options

- `--branch TEXT`: GitHub branch to fetch from (default: main)
- `--save-dir TEXT`: Local directory to save processed data (default: ./data)

### Example

```bash
gitdata --branch main --save-dir ./financial_data
```

Then follow the interactive prompts:

```
🚀 GitData - Financial Data Fetcher
========================================
Enter GitHub username: MapleFrogStudio
Enter repository name: DATA-2025-01
📥 Downloading CSV files from MapleFrogStudio/DATA-2025-01 (branch: main)...
📁 Found 3 CSV files
📊 Processing file: AAPL-2025-01-02.csv
✅ Processed AAPL
📊 Processing file: MSFT-2025-01-02.csv
✅ Processed MSFT
📊 Processing file: TSLA-2025-01-02.csv
✅ Processed TSLA

📈 Processing Summary:
   Files processed: 3
   Files skipped: 0
   Tickers saved: 3

💾 Ticker Summary:
   AAPL.csv (1 files)
   MSFT.csv (1 files)
   TSLA.csv (1 files)

🎉 All files processed. Raw data saved in ./financial_data
```

## Requirements

### Python Version
- Python 3.10+

### Dependencies
- `pandas>=1.3.0` - Data manipulation and CSV processing
- `requests>=2.25.0` - HTTP client for GitHub API interactions
- `click>=8.0.0` - Command-line interface framework

### CSV Data Format

Your CSV files should contain the following columns:

**Required columns:**
- `datetime` - Date/time column (ISO 8601 or common date formats)
- `open` - Opening price
- `high` - Highest price
- `low` - Lowest price  
- `close` - Closing price
- `volume` - Trading volume
- `symbol` or `ticker` - Ticker symbol identifier

**Example CSV structure:**
```csv
datetime,symbol,open,high,low,close,volume
2025-01-02 09:30:00,AAPL,150.00,152.50,149.75,151.25,1000000
2025-01-02 09:31:00,AAPL,151.25,151.75,150.50,151.00,800000
```

## Features

### Data Processing Pipeline

1. **Repository Validation**: Verifies GitHub repository accessibility
2. **File Discovery**: Recursively finds all CSV files in the repository
3. **Content Download**: Downloads file content via GitHub API
4. **Data Consolidation**: Groups by ticker symbol and saves separate files
5. **Raw Data Preservation**: Maintains original data structure without modifications
6. **Output Generation**: Creates organized CSV files in specified directory

### Error Handling

- **Invalid Repository**: Clear error messages for non-existent or private repositories
- **Missing Required Columns**: Skips files missing OHLCV data with warnings
- **Network Issues**: Automatic retry logic with rate limiting handling
- **Data Validation**: Comprehensive validation of datetime and numeric data

### Performance Features

- **Memory Efficient**: Processes files one by one to handle large repositories
- **Rate Limiting**: Includes GitHub API rate limiting protection
- **Resumable**: Can append new data to existing ticker files
- **Scalable**: Handles repositories with hundreds of CSV files

## Output

The tool creates separate CSV files for each ticker symbol:

```
./data/
├── AAPL.csv
├── MSFT.csv
└── TSLA.csv
```

Each output file contains raw CSV data organized by ticker:

```csv
datetime,open,high,low,close,volume
2025-01-02 09:30:00,150.00,152.50,149.75,151.25,1000000
2025-01-02 09:31:00,151.25,151.75,150.50,151.00,800000
```

## Python API

You can also use the package programmatically:

```python
from gitdata import GitHubFetcher, DataProcessor

# Initialize components
fetcher = GitHubFetcher()
processor = DataProcessor(save_dir='./data')

# Fetch CSV files
csv_files = fetcher.fetch_csv_files('username', 'repository', 'main')

# Process each file
for file_info in csv_files:
    result = processor.process_csv_file(file_info)
    if result['success']:
        print(f"Processed {result['ticker']}")
    else:
        print(f"Error: {result['error']}")
```

## License

MIT License

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## Support

For issues and questions, please open an issue on the GitHub repository.
