"""
Command-line interface for gitdata package using Click.
"""

import os
import click
from typing import Optional

from .fetch import GitHubFetcher
from .process import DataProcessor


@click.command()
@click.option('--branch', default='main', help='GitHub branch to fetch from (default: main)')
@click.option('--save-dir', default='./data', help='Local directory to save processed data (default: ./data)')
def gitdata_cli(branch: str, save_dir: str):
    """
    Fetch and consolidate CSV data from GitHub repositories by ticker symbols.
    """
    click.echo("🚀 GitData - Financial Data Fetcher")
    click.echo("=" * 40)
    
    # Get user input
    username = click.prompt("Enter GitHub username", type=str).strip()
    if not username:
        click.echo("❌ Username cannot be empty")
        return
    
    repository = click.prompt("Enter repository name", type=str).strip()
    if not repository:
        click.echo("❌ Repository name cannot be empty")
        return
    
    # Initialize components
    fetcher = GitHubFetcher()
    processor = DataProcessor(save_dir)
    
    try:
        # Create save directory if it doesn't exist
        os.makedirs(save_dir, exist_ok=True)
        
        click.echo(f"\n📥 Downloading CSV files from {username}/{repository} (branch: {branch})...")
        
        # Fetch CSV files from GitHub
        csv_files = fetcher.fetch_csv_files(username, repository, branch)
        
        if not csv_files:
            click.echo("❌ No CSV files found in the repository")
            return
        
        click.echo(f"📁 Found {len(csv_files)} CSV files")
        
        # Process each CSV file
        total_processed = 0
        total_errors = 0
        ticker_stats = {}
        
        for file_info in csv_files:
            try:
                click.echo(f"📊 Processing file: {file_info['name']}")
                
                # Download and process the file
                result = processor.process_csv_file(file_info)
                
                if result['success']:
                    total_processed += 1
                    ticker = result['ticker']
                    
                    if ticker not in ticker_stats:
                        ticker_stats[ticker] = {'files': 0}
                    
                    ticker_stats[ticker]['files'] += 1
                    
                    # Status message
                    click.echo(f"✅ Processed {ticker}")
                else:
                    total_errors += 1
                    click.echo(f"⚠️  Skipped: {result['error']}")
                    
            except Exception as e:
                total_errors += 1
                click.echo(f"❌ Error processing {file_info['name']}: {str(e)}")
        
        # Summary
        click.echo(f"\n📈 Processing Summary:")
        click.echo(f"   Files processed: {total_processed}")
        click.echo(f"   Files skipped: {total_errors}")
        click.echo(f"   Tickers saved: {len(ticker_stats)}")
        
        if ticker_stats:
            click.echo(f"\n💾 Ticker Summary:")
            for ticker, stats in ticker_stats.items():
                click.echo(f"   {ticker}.csv ({stats['files']} files)")
        
        click.echo(f"\n🎉 All files processed. Raw data saved in {save_dir}")
        
    except KeyboardInterrupt:
        click.echo("\n⏹️  Process interrupted by user")
    except Exception as e:
        click.echo(f"\n❌ Unexpected error: {str(e)}")


def main():
    """Entry point for the gitdata CLI."""
    gitdata_cli()


if __name__ == "__main__":
    main()
