import nltk
import re
import os  # For file path manipulation
import csv
import pandas as pd
import time
import requests
from extraction_functions import extract_article_content
from analysis_functions import (
    calculate_positive_score, calculate_negative_score, calculate_polarity_score, calculate_subjectivity_score,
    calculate_average_sentence_length, calculate_percentage_complex_words, calculate_fog_index,
    calculate_word_count, calculate_syllable_per_word, calculate_complex_word_count,
    calculate_personal_pronouns, calculate_average_word_length,
    load_positive_negative_dictionaries, load_stop_words_for_sentiment
)

def analyze_text(text, positive_words, negative_words, stop_words):
    if not text.strip():
        return None  # Handle empty text cases
    
    word_count = calculate_word_count(text)
    positive_score = calculate_positive_score(text, positive_words, stop_words)
    negative_score = calculate_negative_score(text, negative_words, stop_words)
    polarity_score = calculate_polarity_score(positive_score, negative_score)
    subjectivity_score = calculate_subjectivity_score(positive_score, negative_score, word_count)
    avg_sentence_length = calculate_average_sentence_length(text)
    percentage_complex_words = calculate_percentage_complex_words(text)
    fog_index = calculate_fog_index(text)
    syllable_per_word = calculate_syllable_per_word(text)
    complex_word_count = calculate_complex_word_count(text)
    personal_pronouns = calculate_personal_pronouns(text)
    avg_word_length = calculate_average_word_length(text)
    
    return {
        "Positive Score": positive_score,
        "Negative Score": negative_score,
        "Polarity Score": polarity_score,
        "Subjectivity Score": subjectivity_score,
        "Avg Sentence Length": avg_sentence_length,
        "Percentage of Complex Words": percentage_complex_words,
        "Fog Index": fog_index,
        "Avg Number of Words Per Sentence": avg_sentence_length,
        "Complex Word Count": complex_word_count,
        "Word Count": word_count,
        "Syllable Per Word": syllable_per_word,
        "Personal Pronouns": personal_pronouns,
        "Avg Word Length": avg_word_length
    }

def process_url(url_id, url, positive_words, negative_words, stop_words):
    retry_count = 0
    while retry_count < 3:
        try:
            article_data = extract_article_content(url)
            if not article_data:
                print(f"⚠️ Failed to extract content from {url_id} - {url}")
                return None
            
            full_text = " ".join(
                str(section["content"]) for section in article_data
                if isinstance(section, dict) and "content" in section and isinstance(section["content"], str)
            )
            
            if not full_text.strip():
                print(f"⚠️ No meaningful text extracted from {url_id} - {url}")
                return None
            
            print(f"\n✅ Extracted Text for {url_id} (First 500 chars):\n{full_text[:500]}...\n")
            return {"URL": url, **analyze_text(full_text, positive_words, negative_words, stop_words)}
        
        except requests.exceptions.RequestException as e:
            print(f"❌ Request failed for {url_id}, retrying ({retry_count + 1}/3): {e}")
            retry_count += 1
            time.sleep(2 ** retry_count)  # Exponential backoff
    
    print(f"❌ Failed to retrieve content after multiple attempts: {url_id}")
    return None

def main():
    input_file = "data/Input.xlsx"
    output_file = "data/Output Data Structure.xlsx"
    
    print("🚀 Loading dictionaries and stop words...")
    positive_words, negative_words = load_positive_negative_dictionaries(
        "data/dictionaries/positive-words.txt", "data/dictionaries/negative-words.txt"
    )
    stop_words = load_stop_words_for_sentiment("data/StopWords")
    
    print("📂 Reading input file...")
    df = pd.read_excel(input_file)
    results = []
    
    for index, row in df.iterrows():
        url_id, url = row["URL_ID"], row["URL"]
        print(f"🔍 Processing {index + 1}/{len(df)}: {url_id}")
        
        analysis_results = process_url(url_id, url, positive_words, negative_words, stop_words)
        if analysis_results:
            results.append({"URL_ID": url_id, "URL": analysis_results.pop("URL"), **analysis_results})
    
    if results:
        output_df = pd.DataFrame(results)
        with pd.ExcelWriter(output_file, engine='xlsxwriter') as writer:
            output_df.to_excel(writer, index=False, sheet_name='Sheet1')
            workbook = writer.book
            worksheet = writer.sheets['Sheet1']
            url_col_index = output_df.columns.get_loc("URL")
            for row_num in range(1, len(output_df) + 1):
                worksheet.write_url(row_num, url_col_index, output_df.at[row_num - 1, "URL"], string="Click Here")
        print(f"✅ Final output saved to {output_file}")
    else:
        print("⚠️ No valid data to save. Check the logs for issues.")
    
if __name__ == "__main__":
    main()
