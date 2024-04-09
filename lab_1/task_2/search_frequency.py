import json

from collections import defaultdict

from typing import Dict

from constant import Paths2


def read_json_file(file_path: str) -> dict:
    """
    Function to read data from a JSON file.

    Args:
        file_path (str): Path to the JSON file.

    Returns:
        dict: Dictionary containing data from the JSON file.
    """
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)
        return data
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        return {}
    except Exception as e:
        print(f"An unexpected error occurred while reading file '{file_path}': {e}.")
        return {}


def read_text(file: str) -> str:
    """
    Read text from a file.

    Args:
        file (str): file to be read.

    Returns:
        str: file as a string.
    """
    try:
        with open(file, 'r', encoding="utf-8") as filed:
            text = filed.read()
        return text
    except FileNotFoundError:
        print(f"Error: File '{file}' not found.")
        return ""
    except IOError as e:
        print(f"Error reading file '{file}': {e}.")
        return ""


def character_frequency_search(text: str) -> dict:
    """
    Calculate the frequency.

    Args:
        text (str): The text for which character frequencies will be calculated.

    Returns:
        dict: A dictionary containing the frequency of each character in the text.
    """
    try:
        frequency = defaultdict(int)
        for char in text:
            frequency[char] += 1
        return frequency
    except Exception as e:
        print(f"An error occurred during the calculation: {e}")
        return {}


def main()->None:
    """
    A function for working with file paths.

    Parameters: None
    Returns: None
    """
    try:
        json_data = read_json_file(Paths2)
        folder = json_data.get("folder")
        first_file = json_data.get("first_text")
        file = f"{folder}/{first_file}"
        text = read_text(file)
        if text:
            frequency = character_frequency_search(text)
            all_chars = sum(frequency.values())
            sorted_frequency = sorted(
                frequency.items(), key=lambda x: x[1], reverse=True
            )
            for letter, freq in sorted_frequency:
                decimal_freq = freq / all_chars
                print(f"Символ '{letter}': {decimal_freq:.5f}")
    except Exception as e:
        print(f"An error occurred in the main function: {e}")


if __name__ == "__main__":
    main()

