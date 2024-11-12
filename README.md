# jdih-scraper
Indonesian Ministry of Maritime Affairs and Fisheries' JDIH PDF Scraper
Project Name

# Indonesian Fisheries JDIH PDF Scraper

This project is a Python-based web scraper designed to automate the download of legal documents from the Jaringan Dokumentasi dan Informasi Hukum (JDIH) website for Indonesia's Ministry of Maritime Affairs and Fisheries. The script navigates through pages of regulations and downloads PDF files for each document, organizing them for offline access.

## Features
- **Automated PDF Downloading**: Automatically fetches PDFs for Indonesian fisheries laws and regulations.
- **Resumable Downloads**: Maintains a log of downloaded files, allowing resuming from the last saved page.
- **Error Handling**: Manages potential scraping issues like stale elements and click interception for stability.

## Prerequisites
- Python 3.7+
- Google Chrome browser
- ChromeDriver compatible with your Chrome version
- Required Python packages: `selenium`, `webdriver_manager`, and `requests`

## Setup

1. **Clone this repository**:
   ```bash
   git clone https://github.com/FTK6370/jdih-scraper.git
   cd jdih-scraper

    Set up a virtual environment (optional but recommended):

python3 -m venv myenv
source myenv/bin/activate

Install dependencies:

    pip install -r requirements.txt

Configuration

    Download Directory: Update the download_directory variable in scraper.py to specify where PDFs will be saved.
    Target URL: The script is set to navigate the JDIH page for Indonesia's Ministry of Maritime Affairs and Fisheries and retrieve PDF documents from it.

Usage

To start scraping, run:

python scraper.py

Resuming Downloads

The scraper maintains a log of downloaded files in downloaded_pdfs.txt:

    If the script stops, rerun it to resume from the last saved point.
    If you’ve manually downloaded PDFs, run the update_download_log.py helper script to add them to the log.

Error Handling

The scraper includes mechanisms to:

    Retry Clicks: Retries when a download button is blocked by an overlapping element.
    Handle Stale Elements: Refreshes elements that have detached from the DOM.

Limitations

    Requires a reliable internet connection.
    CAPTCHA or rate-limiting measures may stop the script if run for extended periods.

Contributing

Please feel free to open issues or submit pull requests to improve the scraper.
License

This project is licensed under the MIT License.
