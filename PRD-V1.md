# PRD: gitdata

## Overview

`gitdata` is a lightweight Python package designed to fetch, clean, and consolidate financial OHLCV data from public GitHub repositories. It provides a simple console interface where users can specify a GitHub username and repository name containing CSV files of price data. The package downloads, processes, and saves ticker-specific datasets while ensuring data integrity (no duplicate datetime entries).

---

## Objectives

* Provide a simple way to pull financial data hosted on GitHub.
* Ensure data integrity by removing duplicate timestamps.
* Output clean, consolidated CSV files for each ticker symbol.
* Keep the package minimal, focusing on console usability.

---

## Features

### 1. Console Interface

* Prompt user for:

  * GitHub username
  * Repository name
* Optional arguments:

  * Branch (default: `main`)
  * Local save directory (default: `./data`)

### 2. Data Download

* Clone or fetch repository contents using the GitHub API (no authentication required for public repos).
* Identify and download all `.csv` files.
* Process them sequentially (file by file).

### 3. Data Processing

* Assume each CSV contains:

  * `datetime` (ISO 8601 or common date formats)
  * `open`, `high`, `low`, `close`, `volume`
  * `symbol` or `ticker` column
* During processing:

  * Convert `datetime` to a uniform format and set as index.
  * Drop duplicate datetime rows (keep first occurrence).
  * Validate required columns are present.

### 4. Data Consolidation

* Group rows by `ticker`.
* Save each ticker’s clean dataset as a separate CSV file:

  * Output path: `<save_dir>/<TICKER>.csv`
* Append new data if file already exists, ensuring deduplication.

### 5. Error Handling

* If repo is empty or no `.csv` files found → display error message.
* If invalid GitHub user/repo → display error and prompt again.
* Skip files missing required columns, but log a warning.

---

## Technical Requirements

* **Language**: Python 3.10+

* **Dependencies**:

  * `pandas` (data handling)
  * `requests` (GitHub API & file download)
  * `click` (console interface)

* **Data Handling**:

  * Deduplication based on `datetime` index.
  * Assume ticker column is present in each CSV.
  * CSVs must be UTF-8 encoded.

* **Performance**:

  * Process files one by one to avoid memory overload.
  * Handle repos with hundreds of files.

---

## Example Console Flow

```shell
$ gitdata
Enter GitHub username: MapleFrogStudio
Enter repository name: DATA-2025-01
Downloading CSV files...
Processing file: AAPL-2025-01-02.csv
Processing file: MSFT-2025-01-02.csv
Processing file: TSLA-2025-01-02.csv
✅ Saved AAPL.csv (no duplicates)
✅ Saved MSFT.csv (2 duplicates removed)
✅ Saved TSLA.csv (no duplicates)
All files processed. Clean data saved in ./data
```

---

## Deliverables

* Python package `gitdata` with:

  * CLI entry point: `gitdata`
  * Core modules:

    * `fetch.py` (GitHub download logic)
    * `process.py` (data cleaning, deduplication)
    * `cli.py` (console interface with Click)
* Example usage in README.
