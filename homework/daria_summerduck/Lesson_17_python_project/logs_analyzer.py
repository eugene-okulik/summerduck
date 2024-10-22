"""
Logs Analyzer

This script searches for a specified text within log files located in a given directory.
It supports extracting context around the search term and displaying the results.

Usage:
    python logs_analyzer.py --path <logs_directory> --text <search_text> [--first-only]

    path: The directory containing the log files to search.
    text: The text to search for in the log files.
    first-only: Optional flag to return only the first occurrence of the text.

Alternatively, you can set the following environment variables:
    LOGS_PATH: The directory containing the log files to search.
    TEXT: The text to search for in the log files.

Example:
    python logs_analyzer.py --path /var/logs --text "error" --first-only

"""

import os
import re
import argparse
import logging
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(
    level=logging.INFO,  # DEBUG, INFO, WARNING, ERROR, CRITICAL
    format="%(levelname)s - %(message)s",  # Log format
    handlers=[
        logging.StreamHandler(),  # Output logs to the console
    ],
)


# Arguments parsing
def get_arguments() -> argparse.Namespace:
    """
    Parse command line arguments
    :return: parsed arguments
    """
    load_dotenv()
    parser = argparse.ArgumentParser(description="Logs Analyzer")
    parser.add_argument(
        "--path",
        type=str,
        action="store",
        help="Logs path to search",
        default=os.getenv("LOGS_PATH"),
    )
    parser.add_argument(
        "--text",
        type=str,
        action="store",
        help="Text to search",
        default=os.getenv("TEXT"),
    )
    parser.add_argument(
        "--first-only",
        action="store",
        help="Return only the first occurrence of the text.",
        default=False,
    )
    return parser.parse_args()


def search_text_in_file(file_path, text_to_search, first_only=False) -> list:
    """
    Search text in file
    :param file_path: path to file
    :param text_to_search: text to search
    :param first_only: return only the first occurrence
    :return: list of found lines
    """
    found_lines = []
    try:
        with open(file_path, "r") as file:
            number = 0
            for line_number, line in enumerate(file):
                if re.search(text_to_search, line):
                    found_lines.append((line_number, line))
                    logging.debug(
                        f"Found {text_to_search} in {file_path} at line {line_number}"
                    )
                    logging.debug(f"Number of occurrences found so far: {number + 1}")
                    number += 1
                    if first_only:
                        logging.debug(
                            f"Returning only the first occurrence of {text_to_search}"
                        )
                        break
    except FileNotFoundError:
        raise FileNotFoundError(f"File not found: {file_path}")
    except Exception as e:
        raise Exception(f"Error reading file {file_path}: {e}")

    return found_lines


def extract_context(line, search_term, context_words=5):
    """
    Extract a context of words around the search term.
    :param line: The line containing the search term.
    :param search_term: The term to search for in the line.
    :param context_words: Number of words to show before and after the term.
    :return: The line with context around the search term.
    """
    try:
        words = line.split()
        if search_term not in words:
            raise ValueError(f"Search term '{search_term}' not found in line.")
        index = words.index(search_term)
        start = max(index - context_words, 0)
        end = min(index + context_words + 1, len(words))
        return " ".join(words[start:end])
    except ValueError:
        logging.error(f"Failed to extract context for {search_term} in line {line}")
        return None


def display_search_results(file_path, found_lines, search_term):
    """
    Display the results of the search.
    :param file_path: Path to the file.
    :param found_lines: List of found lines with their line numbers.
    :param search_term: The search term to highlight in the output.
    """
    if not found_lines:
        logging.info(f"No occurrences found in {file_path}.")
    for line_number, line in found_lines:
        context = extract_context(line, search_term)
        logging.warning(
            f"\nFile: {file_path}, \nLine: {line_number}, \nContext: '{context}' \n"
        )


def verify_path(path):
    """
    Verify that the path exists.
    :param args: The parsed command line arguments.
    """
    if not os.path.exists(path):
        raise OSError(f"Error: The directory {path} does not exist.")


def main():
    args = get_arguments()

    verify_path(args.path)

    for root, _, files in os.walk(args.path):
        for file in files:
            file_path = os.path.join(root, file)

            found_lines = search_text_in_file(file_path, args.text, args.first_only)

            display_search_results(file_path, found_lines, args.text)


if __name__ == "__main__":
    main()
