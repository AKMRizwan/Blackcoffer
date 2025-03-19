# Approach to the Solution

# 1. Understanding the Requirements
We first carefully analyzed the assignment requirements, including the Input.xlsx structure and expected Output Data Structure.xlsx. We also studied the Text Analysis document to understand how each metric (positive score, fog index, subjectivity, etc.) should be calculated.

# 2. Setting Up the Environment
Created a virtual environment to manage dependencies efficiently.
Installed essential libraries such as pandas, requests, beautifulsoup4, nltk, and openpyxl.
Organized project files into structured directories: data/, scripts/, and documentation/.
# 3. Data Extraction
Reading Input.xlsx: Loaded the URL list using pandas.
Web Scraping: Implemented web scraping using requests and BeautifulSoup to extract article text.
Handling Errors: Added retry mechanisms for failed requests and timeouts.
# 4. Text Analysis
Implemented various NLP techniques using NLTK:

Sentiment Analysis: Used predefined positive and negative word dictionaries to compute sentiment scores.
Text Complexity Analysis: Calculated metrics like fog index, complex words, and syllables per word.
Linguistic Features: Extracted word count, sentence length, and personal pronoun occurrences.
# 5. Generating Output
Processed data was structured into a pandas DataFrame.
URLs were formatted as clickable links in the output Excel file.
The final data was exported to Output Data Structure.xlsx using XlsxWriter.
# 6. Testing & Debugging
Verified outputs for multiple URLs.
Fixed issues such as non-extractable content, incorrect personal pronoun detection, and Excel formatting.
Ensured the script runs end-to-end without manual intervention.
