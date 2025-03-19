Data Extraction and Sentiment Analysis Project

Project Overview

This project automates the extraction of text data from a list of URLs, analyzes the extracted content, and generates a structured output file with various sentiment and linguistic metrics. The analysis includes calculating polarity scores, subjectivity, word complexity, sentence structures, and more. The final processed data is saved in an Excel file for further insights.

Features

Web scraping to extract text from URLs.

Sentiment analysis using predefined positive and negative word dictionaries.

Text complexity analysis including fog index, word count, and sentence structures.

Output formatted as an Excel file with clickable URLs.

Installation Guide

Prerequisites

Python 3.x installed

A virtual environment (recommended for dependency isolation)

Setup

Clone the repository or download the project files.

Navigate to the project directory in the terminal:

cd path/to/project

Create and activate a virtual environment:

Windows:

python -m venv venv
venv\Scripts\activate

macOS/Linux:

python3 -m venv venv
source venv/bin/activate

Install the required dependencies:

pip install -r requirements.txt

Execution Steps

Place Input.xlsx (containing URLs) in the data/ directory.

Run the main script to start extraction and analysis:

python main_script.py

The output file Output Data Structure.xlsx will be generated in the data/ directory.

Dependencies

pandas - For reading and writing Excel files.

openpyxl - For handling Excel file operations.

requests - For fetching web page content.

beautifulsoup4 - For parsing HTML and extracting text.

nltk - For natural language processing and sentiment analysis.

xlsxwriter - For formatting Excel files.

Output Explanation

The output Excel file contains the following columns:

URL_ID: Unique identifier for each URL.

URL: Clickable hyperlink to the extracted webpage.

Positive Score: Count of positive words in the text.

Negative Score: Count of negative words in the text.

Polarity Score: Measure of positivity/negativity.

Subjectivity Score: Extent of personal opinion in the text.

Avg Sentence Length: Average number of words per sentence.

Percentage of Complex Words: Complexity measure of the text.

Fog Index: Readability score based on word complexity.

Word Count: Total number of words.

Syllable Per Word: Average syllables per word.

Complex Word Count: Count of complex words in the text.

Avg Word Length: Average length of words in the text.

Common Errors & Fixes

Permission Denied on Output File: Close any open Excel files before running the script.

Request Timeouts on URL Extraction: The script retries failed requests up to 3 times.

Contact

For any issues, feel free to raise a query in the repository or contact the project maintainers.
