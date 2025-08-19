"""
Data processing logic for cleaning and consolidating financial OHLCV data.
"""

import pandas as pd
import os
from typing import Dict, Optional, List
from io import StringIO
import warnings

from .fetch import GitHubFetcher


class DataProcessor:
    """
    Handles processing and consolidation of CSV data by ticker symbols without modification.
    """
    
    def __init__(self, save_dir: str = "./data"):
        """
        Initialize the data processor.
        
        Args:
            save_dir: Directory to save processed CSV files
        """
        self.save_dir = save_dir
        self.fetcher = GitHubFetcher()
        
        # Possible ticker column names
        self.ticker_columns = ['symbol', 'ticker', 'Symbol', 'Ticker', 'SYMBOL', 'TICKER']
        
        # Suppress pandas warnings for cleaner output
        warnings.filterwarnings('ignore', category=pd.errors.DtypeWarning)
    
    def process_csv_file(self, file_info: Dict) -> Dict:
        """
        Process a single CSV file: download, clean, and save by ticker.
        
        Args:
            file_info: Dictionary containing file information from GitHub
            
        Returns:
            Dictionary with processing results
        """
        try:
            # Download file content
            csv_content = self.fetcher.download_csv_content(file_info['download_url'])
            
            # Parse CSV content
            df = pd.read_csv(StringIO(csv_content))
            
            if df.empty:
                return {
                    'success': False,
                    'error': f"File {file_info['name']} is empty"
                }
            
            # Validate and clean the data
            cleaned_df = self._clean_dataframe(df, file_info['name'])
            
            if cleaned_df is None or cleaned_df.empty:
                return {
                    'success': False,
                    'error': f"File {file_info['name']} has no valid data after cleaning"
                }
            
            # Process each ticker in the file
            results = self._process_tickers(cleaned_df, file_info['name'])
            
            if not results:
                return {
                    'success': False,
                    'error': f"No valid ticker data found in {file_info['name']}"
                }
            
            # Return success with the first ticker's info (for display purposes)
            first_result = list(results.values())[0]
            return {
                'success': True,
                'ticker': first_result['ticker'],
                'duplicates_removed': first_result['duplicates_removed'],
                'rows_processed': first_result['rows_processed']
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': f"Error processing {file_info['name']}: {str(e)}"
            }
    
    def _clean_dataframe(self, df: pd.DataFrame, filename: str) -> Optional[pd.DataFrame]:
        """
        Validate a DataFrame and identify ticker column.
        
        Args:
            df: Raw DataFrame from CSV
            filename: Name of the source file for error reporting
            
        Returns:
            DataFrame with ticker column identified or None if validation fails
        """
        try:
            # Check for ticker column
            ticker_col = None
            for ticker_name in self.ticker_columns:
                if ticker_name in df.columns:
                    ticker_col = ticker_name
                    break
            
            if ticker_col is None:
                print(f"Warning: File {filename} missing ticker/symbol column")
                return None
            
            # Rename ticker column to standard name for consistency
            if ticker_col != 'ticker':
                df = df.rename(columns={ticker_col: 'ticker'})
            
            return df
            
        except Exception as e:
            print(f"Warning: Error processing {filename}: {str(e)}")
            return None
    
    def _process_tickers(self, df: pd.DataFrame, filename: str) -> Dict:
        """
        Process data for each ticker and save to separate files without any modifications.
        
        Args:
            df: DataFrame with ticker data
            filename: Source filename for logging
            
        Returns:
            Dictionary with processing results for each ticker
        """
        results = {}
        
        # Group by ticker
        ticker_groups = df.groupby('ticker')
        
        for ticker, ticker_df in ticker_groups:
            try:
                # Remove ticker column from the data (it's redundant now)
                ticker_data = ticker_df.drop(columns=['ticker'])
                
                # Save to file
                output_file = os.path.join(self.save_dir, f"{ticker}.csv")
                
                if os.path.exists(output_file):
                    # Append to existing file without any processing
                    ticker_data.to_csv(output_file, mode='a', header=False)
                else:
                    # Save new file
                    ticker_data.to_csv(output_file)
                
                results[ticker] = {
                    'ticker': ticker,
                    'rows_processed': len(ticker_data),
                    'duplicates_removed': 0,  # No duplicate removal
                    'output_file': output_file
                }
                
            except Exception as e:
                print(f"Warning: Error processing ticker {ticker} from {filename}: {str(e)}")
                continue
        
        return results
    
    def get_ticker_summary(self) -> Dict:
        """
        Get summary information about all processed ticker files.
        
        Returns:
            Dictionary with ticker file information
        """
        summary = {}
        
        if not os.path.exists(self.save_dir):
            return summary
        
        for filename in os.listdir(self.save_dir):
            if filename.endswith('.csv'):
                ticker = filename[:-4]  # Remove .csv extension
                filepath = os.path.join(self.save_dir, filename)
                
                try:
                    df = pd.read_csv(filepath)
                    summary[ticker] = {
                        'rows': len(df),
                        'file_size': os.path.getsize(filepath)
                    }
                except Exception as e:
                    summary[ticker] = {
                        'error': f"Could not read file: {str(e)}"
                    }
        
        return summary
