# analysis_functions.py
import nltk
import re
import os  # For file path manipulation
from nltk.corpus import stopwords

nltk.download('punkt')

def calculate_average_sentence_length(text):
    """
    Calculates the average sentence length of a text.

    Args:
        text (str): The input text.

    Returns:
        float: The average sentence length (words per sentence), or 0 if no sentences.
    """
    sentences = nltk.sent_tokenize(text)
    if not sentences:
        return 0  
    word_count = sum(len(nltk.word_tokenize(sentence)) for sentence in sentences)
    return word_count / len(sentences)

def calculate_word_count(text):
    """
    Calculates the word count of a text after removing stop words and punctuation.

    Args:
        text (str): The input text.

    Returns:
        int: The cleaned word count.
    """
    stop_words = set(stopwords.words('english'))
    words = nltk.word_tokenize(text.lower())
    cleaned_words = [word for word in words if word.isalpha() and word not in stop_words]
    return len(cleaned_words)

def calculate_average_word_length(text):
    """
    Calculates the average word length in a text after cleaning.

    Args:
        text (str): The input text.

    Returns:
        float: The average word length.
    """
    words = nltk.word_tokenize(text.lower())
    cleaned_words = [word for word in words if word.isalpha()]
    if not cleaned_words:
        return 0
    total_char_count = sum(len(word) for word in cleaned_words)
    return total_char_count / len(cleaned_words)

def count_syllables(word):
    """
    Counts syllables in a word.

    Args:
        word (str): The word to analyze.

    Returns:
        int: The syllable count.
    """
    word = word.lower()
    vowels = "aeiouy"
    syllable_count = 0
    prev_char_was_vowel = False

    for char in word:
        if char in vowels:
            if not prev_char_was_vowel:
                syllable_count += 1
            prev_char_was_vowel = True
        else:
            prev_char_was_vowel = False

    return max(syllable_count, 1)

def calculate_syllable_per_word(text):
    """
    Calculates the average number of syllables per word.

    Args:
        text (str): The input text.

    Returns:
        float: The average syllables per word.
    """
    words = nltk.word_tokenize(text.lower())
    total_syllables = sum(count_syllables(word) for word in words if word.isalpha())
    total_words = len([word for word in words if word.isalpha()])

    return total_syllables / total_words if total_words > 0 else 0

def calculate_complex_word_count(text):
    """
    Counts complex words (words with more than 2 syllables).

    Args:
        text (str): The input text.

    Returns:
        int: The count of complex words.
    """
    words = nltk.word_tokenize(text.lower())
    cleaned_words = [word for word in words if word.isalpha()]
    return sum(1 for word in cleaned_words if count_syllables(word) > 2)

def calculate_percentage_complex_words(text):
    """
    Calculates the percentage of complex words in a text.

    Args:
        text (str): The input text.

    Returns:
        float: The percentage of complex words.
    """
    word_count = calculate_word_count(text)
    complex_word_count = calculate_complex_word_count(text)

    return (complex_word_count / word_count) * 100 if word_count > 0 else 0

def calculate_fog_index(text):
    """
    Calculates the Gunning Fog Index.

    Args:
        text (str): The input text.

    Returns:
        float: The Fog Index score.
    """
    avg_sentence_length = calculate_average_sentence_length(text)
    percentage_complex_words = calculate_percentage_complex_words(text)

    return 0.4 * (avg_sentence_length + percentage_complex_words)

# def calculate_personal_pronouns(text):
#     """
#     Counts personal pronouns in the text while ensuring correct word boundaries and case insensitivity.

#     Args:
#         text (str): The input text.

#     Returns:
#         int: The count of personal pronouns.
#     """
#     personal_pronouns = [
#         "I", "we", "my", "ours", "us", "you", "your", "yours",
#         "he", "she", "him", "her", "they", "them", "their", "theirs", "me"
#     ]
    
#     # Ensure word boundaries (\b) and allow for punctuation like commas or periods after words
#     pattern = r'\b(?:' + '|'.join(personal_pronouns) + r')\b'

#     # Use re.IGNORECASE to count both lowercase and uppercase versions
#     matches = re.findall(pattern, text, re.IGNORECASE)
    
#     return len(matches)
def calculate_personal_pronouns(text):
    """
    Counts personal pronouns in the text using word tokenization.
    """
    personal_pronouns = {"i", "we", "my", "ours", "us", "you", "your", "yours", "he", "she", "him", "her", "they", "them", "their", "theirs", "me"}
    words = nltk.word_tokenize(text)
    pronoun_count = sum(1 for word in words if word.lower() in personal_pronouns)
    return pronoun_count

def load_positive_negative_dictionaries(positive_words_file_path, negative_words_file_path):
    """
    Loads positive and negative words from text files.

    Args:
        positive_words_file_path (str): Path to the positive-words.txt file.
        negative_words_file_path (str): Path to the negative-words.txt file.

    Returns:
        tuple: (positive_words_set, negative_words_set).
    """
    positive_words = set()
    negative_words = set()

    try:
        with open(positive_words_file_path, 'r', encoding='utf-8', errors='ignore') as f:
            for line in f:
                word = line.strip().lower()
                if word:
                    positive_words.add(word)
    except FileNotFoundError:
        print(f"Error: Positive words file not found at {positive_words_file_path}")
        return set(), set()

    try:
        with open(negative_words_file_path, 'r', encoding='utf-8', errors='ignore') as f:
            for line in f:
                word = line.strip().lower()
                if word:
                    negative_words.add(word)
    except FileNotFoundError:
        print(f"Error: Negative words file not found at {negative_words_file_path}")
        return set(), set()

    return positive_words, negative_words

def load_stop_words_for_sentiment(stopwords_dir_path):
    """
    Loads stop words from .txt files in the specified directory.

    Args:
        stopwords_dir_path (str): Path to the StopWords directory.

    Returns:
        set: A set of stop words.
    """
    stop_words = set()
    stopwords_files = [f for f in os.listdir(stopwords_dir_path) if f.endswith('.txt')]

    for file_name in stopwords_files:
        file_path = os.path.join(stopwords_dir_path, file_name)
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                for line in f:
                    word = line.strip().lower()
                    if word:
                        stop_words.add(word)
        except FileNotFoundError:
            print(f"Error: Stop words file not found at {file_path}")

    return stop_words

def calculate_positive_score(text, positive_words, stop_words_sentiment):
    """
    Calculates the Positive Score.

    Args:
        text (str): The input text.
        positive_words (set): Set of positive words.
        stop_words_sentiment (set): Set of stop words.

    Returns:
        int: The Positive Score.
    """
    words = nltk.word_tokenize(text.lower())
    cleaned_words = [word for word in words if word.isalpha() and word not in stop_words_sentiment]
    return sum(1 for word in cleaned_words if word in positive_words)

def calculate_negative_score(text, negative_words, stop_words_sentiment):
    """
    Calculates the Negative Score.

    Args:
        text (str): The input text.
        negative_words (set): Set of negative words.
        stop_words_sentiment (set): Set of stop words.

    Returns:
        int: The Negative Score.
    """
    words = nltk.word_tokenize(text.lower())
    cleaned_words = [word for word in words if word.isalpha() and word not in stop_words_sentiment]
    return sum(1 for word in cleaned_words if word in negative_words)

def calculate_polarity_score(positive_score, negative_score):
    """
    Calculates the Polarity Score.

    Returns:
        float: The Polarity Score.
    """
    return (positive_score - negative_score) / ((positive_score + negative_score) + 0.000001)

def calculate_subjectivity_score(positive_score, negative_score, total_words):
    """
    Calculates the Subjectivity Score.

    Returns:
        float: The Subjectivity Score.
    """
    return (positive_score + negative_score) / (total_words + 0.000001)
