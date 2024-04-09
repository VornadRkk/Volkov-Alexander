import json

from constant import Alphavit, Paths, shift


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


def ceasar_encrypt(text: str, shift: int) -> str:
    """
    Encrypts the given text using the Caesar cipher with the specified shift.

    Args:
        text (str): The text to be encrypted.
        shift (int): The shift value for the Caesar cipher.

    Returns:
        str: The encrypted text.
    """
    encrypted_text = ""
    text = text.upper()
    for x in text:
        if x.isalpha():
                ind = Alphavit.index(x)
                encrypted_text += Alphavit[(ind + shift) % len(Alphavit)]
        else:
            encrypted_text += x
    return encrypted_text


def main() -> None:
    """
    A function for working with file paths.
    """
    paths_data = read_json_file(Paths)
    if paths_data:
        folder = paths_data.get("folder", "")
        first_text = paths_data.get("first_text", "")
        second_text = paths_data.get("second_text", "")

        if folder and first_text and second_text:
            with open(f"{folder}/{first_text}", "r", encoding="utf-8") as file:
                text = file.read()
                encrypted_text = ceasar_encrypt(text, shift)

            with open(f"{folder}/{second_text}", "w", encoding="utf-8") as file:
                file.write(encrypted_text)


if __name__ == "__main__":
    main()
    
