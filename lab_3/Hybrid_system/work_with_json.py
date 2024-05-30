import json


class WorkFile:
    """
    Utility class for reading from and writing to files.

    This class provides static methods for reading JSON files, text files,
    writing text files, and writing bytes data to files.
    """

    @staticmethod
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
            print(
                f"An unexpected error occurred while reading file '{file_path}': {e}."
            )
            return {}

    @staticmethod
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
            print(
                f"An unexpected error occurred while reading file '{file_path}': {e}."
            )
            return ""

    @staticmethod
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
            print(
                f"An unexpected error occurred while writing to file '{file_path}': {e}."
            )

    @staticmethod
    def write_bytes_to_file(file_path: str, bytes_data: bytes) -> None:
        """
        Write bytes data to a file.

        Args:
            file_path (str): Path to the file.
            bytes_data (bytes): Bytes data to be written to the file.

        Returns:
            None
        """
        try:
            with open(file_path, "wb") as file:
                file.write(bytes_data)
            print(f"Bytes data written to '{file_path}' successfully.")
        except Exception as e:
            raise RuntimeError(f"Error writing bytes data to file '{file_path}': {e}")

    @staticmethod
    def read_key_bytes(file_path: str) -> bytes:
        """
        method for reading key
        parametrs: file_path as str
        return: bytes
        """
        try:
            with open(file_path, "rb") as file:
                data = file.read()
            return data
        except FileNotFoundError:
            print("File not found.")
            return b""
