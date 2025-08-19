"""
GitHub fetching logic for downloading CSV files from public repositories.
"""

import requests
import base64
from typing import List, Dict, Optional
import time


class GitHubFetcher:
    """
    Handles fetching CSV files from GitHub repositories using the GitHub API.
    """
    
    def __init__(self):
        self.base_url = "https://api.github.com"
        self.session = requests.Session()
        # Set a user agent to avoid rate limiting issues
        self.session.headers.update({
            'User-Agent': 'gitdata/1.0.0'
        })
    
    def fetch_csv_files(self, username: str, repository: str, branch: str = "main") -> List[Dict]:
        """
        Fetch all CSV files from a GitHub repository.
        
        Args:
            username: GitHub username
            repository: Repository name
            branch: Branch name (default: main)
            
        Returns:
            List of dictionaries containing file information
            
        Raises:
            Exception: If repository is invalid or inaccessible
        """
        csv_files = []
        
        try:
            # First, verify the repository exists
            repo_url = f"{self.base_url}/repos/{username}/{repository}"
            repo_response = self._make_request(repo_url)
            
            if repo_response.status_code == 404:
                raise Exception(f"Repository {username}/{repository} not found or is not public")
            elif repo_response.status_code != 200:
                raise Exception(f"Failed to access repository: HTTP {repo_response.status_code}")
            
            # Get repository contents recursively
            csv_files = self._get_csv_files_recursive(username, repository, branch, "")
            
            return csv_files
            
        except requests.exceptions.RequestException as e:
            raise Exception(f"Network error while accessing GitHub: {str(e)}")
    
    def _get_csv_files_recursive(self, username: str, repository: str, branch: str, path: str) -> List[Dict]:
        """
        Recursively search for CSV files in the repository.
        
        Args:
            username: GitHub username
            repository: Repository name
            branch: Branch name
            path: Current path in the repository
            
        Returns:
            List of CSV file information dictionaries
        """
        csv_files = []
        
        try:
            # Get contents of current directory
            contents_url = f"{self.base_url}/repos/{username}/{repository}/contents/{path}"
            if branch != "main":
                contents_url += f"?ref={branch}"
            
            response = self._make_request(contents_url)
            
            if response.status_code != 200:
                return csv_files
            
            contents = response.json()
            
            # Handle single file response (when path points to a file)
            if isinstance(contents, dict):
                contents = [contents]
            
            for item in contents:
                if item['type'] == 'file' and item['name'].lower().endswith('.csv'):
                    # This is a CSV file
                    csv_files.append({
                        'name': item['name'],
                        'path': item['path'],
                        'download_url': item['download_url'],
                        'size': item['size']
                    })
                elif item['type'] == 'dir':
                    # Recursively search subdirectories
                    sub_csv_files = self._get_csv_files_recursive(
                        username, repository, branch, item['path']
                    )
                    csv_files.extend(sub_csv_files)
            
            return csv_files
            
        except requests.exceptions.RequestException as e:
            # Log the error but continue processing other directories
            print(f"Warning: Could not access directory {path}: {str(e)}")
            return csv_files
    
    def download_csv_content(self, download_url: str) -> str:
        """
        Download CSV file content from GitHub.
        
        Args:
            download_url: Direct download URL for the CSV file
            
        Returns:
            CSV content as string
            
        Raises:
            Exception: If download fails
        """
        try:
            response = self._make_request(download_url)
            
            if response.status_code != 200:
                raise Exception(f"Failed to download file: HTTP {response.status_code}")
            
            # Ensure content is decoded as UTF-8
            response.encoding = 'utf-8'
            return response.text
            
        except requests.exceptions.RequestException as e:
            raise Exception(f"Network error while downloading file: {str(e)}")
    
    def _make_request(self, url: str, max_retries: int = 3) -> requests.Response:
        """
        Make a request with retry logic for rate limiting.
        
        Args:
            url: URL to request
            max_retries: Maximum number of retries
            
        Returns:
            Response object
        """
        for attempt in range(max_retries):
            try:
                response = self.session.get(url, timeout=30)
                
                # Handle rate limiting
                if response.status_code == 403 and 'rate limit' in response.text.lower():
                    if attempt < max_retries - 1:
                        # Wait and retry
                        wait_time = 60  # Wait 1 minute for rate limit reset
                        print(f"Rate limited. Waiting {wait_time} seconds before retry...")
                        time.sleep(wait_time)
                        continue
                    else:
                        raise Exception("GitHub API rate limit exceeded. Please try again later.")
                
                return response
                
            except requests.exceptions.Timeout:
                if attempt < max_retries - 1:
                    print(f"Request timeout. Retrying... (attempt {attempt + 1}/{max_retries})")
                    time.sleep(2)
                    continue
                else:
                    raise
            
            except requests.exceptions.RequestException as e:
                if attempt < max_retries - 1:
                    print(f"Request failed. Retrying... (attempt {attempt + 1}/{max_retries})")
                    time.sleep(2)
                    continue
                else:
                    raise
        
        # This should never be reached, but just in case
        raise Exception("Maximum retries exceeded")
