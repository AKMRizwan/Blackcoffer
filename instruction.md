# Instructions

## Approach to the Solution

1. **Reading Input**: The script reads URLs from an input Excel file named `Input.xlsx` located in the `data` directory.
2. **Extracting Text**: For each URL, the script fetches the webpage content and extracts the text using BeautifulSoup.
3. **Sentiment Analysis**: The script uses NLTK's VADER sentiment analyzer to compute positive, negative, polarity, and subjectivity scores.
4. **Text Complexity Analysis**: The script calculates various text complexity metrics like average sentence length, complex word count, and fog index.
5. **Output**: The results are written to an Excel file named `Output Data Structure.xlsx` in the `data` directory.

## How to Run the Script

1. **Setup**:
   - Ensure Python 3.x is installed.
   - Create and activate a virtual environment (recommended).

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install Dependencies:
   pip install -r requirements.txt

# Run the script
   Ensure Input.xlsx is placed in the data/ directory. Then, run the script:
   python main_script.py

# Output:

The output will be generated as Output Data Structure.xlsx in the data/ directory.

# Dependencies
pandas
openpyxl
requests
beautifulsoup4
nltk
xlsxwriter


### Summary of Deliverables
- `main_script.py`: The Python script for data extraction and analysis.
- `requirements.txt`: File listing all dependencies.
- `instructions.md`: Documentation explaining the approach, how to run the script, and dependencies.

Follow these steps to create the necessary files and ensure they meet the outlined requirements. If you need further assistance, feel free to ask!
