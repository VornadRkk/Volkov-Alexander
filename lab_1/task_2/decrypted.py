from constant import Paths2, Alphavit

from search_frequency import read_text, read_json_file


def decrypt_text(text: str, change: dict) -> str:
    """
    Decrypt the text using the given cipher.

    Args:
        text (str): The text to be decrypted.
        cipher (dict): The decryption cipher, where keys are encrypted characters
                       and values are their corresponding decrypted characters.

    Returns:
        str: The decrypted text.
    """
    try:
        decrypted_text = ""
        for char in text:
            decrypted_text += change.get(char, char)
        return decrypted_text
    except Exception as e:
        print(f"An error occurred during text decryption: {e}")
        return ""


def main() -> None:
    """
    A function for working with file paths.

    Parameters: None
    Returns: None
    """
    try:
        json_data = read_json_file(Paths2)
        if json_data:
            folder = json_data.get("folder", "")
            first_text = json_data.get("first_text", "")
            second_text = json_data.get("second_text", "")
            input_file = f"{folder}/{first_text}"
            output_file = f"{folder}/{second_text}"

            text = read_text(input_file)
            if text:
                decrypted_text = decrypt_text(text, Alphavit)
                with open(output_file, "w", encoding="utf-8") as file:
                    file.write(decrypted_text)
                    print(f"Decrypted text '{output_file}'")
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
