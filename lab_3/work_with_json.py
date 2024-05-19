import json


class WorkFile:

    def read_json_file(file_path: str) -> dict:
        """
        Function to read data from a JSON file.

        Args:
            file_path (str): Path to the JSON file.

        Returns:
            dict: Dictionaryy containing data from the JSON file.
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
        
    def read_text_file(file_path: str) -> str:
        """
        Function to read data from a text file.

        Args:
            file_path (str): Path to the text file.

        Returns:
            str: Content of the text file.
        """
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                content = file.read()
            return content
        except FileNotFoundError:
            print(f"Error: File '{file_path}' not found.")
            return ""
        except Exception as e:
            print(f"An unexpected error occurred while reading file '{file_path}': {e}.")
            return ""

    def write_text_file(content: str, file_path: str) -> None:
        """
        Function to write data to a text file.

        Args:
            content (str): Content to be written to the text file.
            file_path (str): Path to the text file.
        """
        try:
            with open(file_path, "w", encoding="utf-8") as file:
                file.write(content)
            print(f"Content successfully written to '{file_path}'.")
        except Exception as e:
            print(f"An unexpected error occurred while writing to file '{file_path}': {e}.")