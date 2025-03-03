import os
import socket
from collections import Counter
import re

# List of common contractions
CONTRACTIONS_DICT = {
    "I'm": "I am", "I'll": "I will", "can't": "cannot", "couldn't": "could not",
    "won't": "will not", "don't": "do not", "you're": "you are", "wanna": "want to",
    "that's": "that is", "it's": "it is"
}

# Common stop words to exclude from frequency count
STOP_WORDS = {"i", "the", "will", "is", "it", "a", "an", "and", "to", "of", "in", "on", "for"}

def expand_contractions(text):
    """Replace contractions in text using the predefined dictionary."""
    for contraction, full_form in CONTRACTIONS_DICT.items():
        text = text.replace(contraction, full_form)
    return text

def clean_and_split_text(text):
    """Convert text to lowercase, remove punctuation, and split into words."""
    text = expand_contractions(text)
    text = text.lower()  # Make case insensitive
    text = re.sub(r'[^a-z\s]', '', text)  # Remove punctuation
    words = text.split()  # Split into words
    return words

def process_file_content(file_path, split_contractions=False):
    """Read and process text file, returning word counts."""
    try:
        with open(file_path, 'r') as file:
            text = file.read()

        total_words_before = len(text.split())  # Original word count before processing

        words = clean_and_split_text(text) if split_contractions else text.lower().split()

        # Filter out stop words
        words = [word for word in words if word not in STOP_WORDS]

        word_counts = Counter(words)  # Count word frequencies

        return total_words_before, word_counts

    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return 0, Counter()
    except Exception as e:
        print(f"Error processing file {file_path}: {e}")
        return 0, Counter()

def write_results_to_file(results):
    """Save results to an output file."""
    output_dir = '/home/data/output'
    os.makedirs(output_dir, exist_ok=True)

    result_file_path = os.path.join(output_dir, 'result.txt')

    try:
        with open(result_file_path, 'w') as result_file:
            result_file.write(results)
        print(f"Results written to {result_file_path}")
    except Exception as e:
        print(f"Error writing results: {e}")

    return result_file_path

def get_ip_address():
    """Retrieve the IP address of the container."""
    try:
        return socket.gethostbyname(socket.gethostname())
    except Exception as e:
        print(f"Error getting IP address: {e}")
        return "Unknown"

def main():
    """Main function to process files and display results."""
    try:
        if_file_path = '/home/data/IF.txt' 
        always_remember_file_path = '/home/data/AlwaysRememberUsThisWay.txt'

        # Process "IF.txt" without expanding contractions
        total_words_if, word_counts_if = process_file_content(if_file_path)
        top_3_if = word_counts_if.most_common(3)

        # Process "AlwaysRememberUsThisWay.txt" with contraction expansion
        total_words_always_remember, word_counts_always_remember = process_file_content(always_remember_file_path, split_contractions=True)
        top_3_always_remember = word_counts_always_remember.most_common(3)

        # Calculate total words across both files
        grand_total_words = total_words_if + total_words_always_remember

        # Get container IP
        ip_address = get_ip_address()

        # Format results
        results = (
            f"Results for IF.txt:\n"
            f"Total words: {total_words_if}\n"
            f"Top 3 most frequent words:\n"
        )
        for word, count in top_3_if:
            results += f"{word}: {count}\n"

        results += (
            f"\nResults for AlwaysRememberUsThisWay.txt:\n"
            f"Total words before splitting contractions: {total_words_always_remember}\n"
            f"Top 3 most frequent words:\n"
        )
        for word, count in top_3_always_remember:
            results += f"{word}: {count}\n"

        results += f"\nGrand total of words across both files: {grand_total_words}\n"
        results += f"IP Address of the container: {ip_address}\n"

        # Write results to file and print to console
        result_file_path = write_results_to_file(results)

        with open(result_file_path, 'r') as result_file:
            print(result_file.read())

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
