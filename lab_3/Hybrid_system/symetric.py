import os


class Symetric:
    """
    A class for generating, serializing, and deserializing symmetric keys (3DES).

    Attributes:
        None

    Methods:
        generate_symmetric_key(key_length: int) -> bytes:
            Generate a 3DES key with a specified length.

        serialize_symmetric_key(symmetric_key: bytes, file_path: str) -> None:
            Serialize a symmetric key to a file.

        deserialize_symmetric_key(file_path: str) -> bytes:
            Deserialize a symmetric key from a file.
    """

    @staticmethod
    def generate_symetric_key(key_length: int) -> bytes:
        """
        Generate a 3DES key with a specified length.

        Args:
            key_length (int): Length of the key in bits (64, 128, or 192).

        Returns:
            bytes: 3DES key.
        """
        if key_length not in [64, 128, 192]:
            raise ValueError("Key length must be 64, 128, or 192 bits.")

        try:
            if key_length == 64:
                return os.urandom(8) * 2
            elif key_length == 128:
                return os.urandom(16)
            elif key_length == 192:
                return os.urandom(24)
        except Exception as e:
            raise RuntimeError(f"Error generating 3DES key: {e}")

    @staticmethod
    def serialize_symmetric_key(symmetric_key: bytes, file_path: str) -> None:
        """
        Serialize a symmetric key to a file.

        Args:
            symmetric_key (bytes): Symmetric key to be serialized.
            file_path (str): Path to the file.
        """
        try:
            with open(file_path, "wb") as file:
                file.write(symmetric_key)
        except Exception as e:
            raise RuntimeError(
                f"Error serializing symmetric key to file '{file_path}': {e}"
            )

    @staticmethod
    def deserialize_symmetric_key(file_path: str) -> bytes:
        """
        Deserialize a symmetric key from a file.

        Args:
            file_path (str): Path to the file containing the serialized key.

        Returns:
            bytes: Deserialized symmetric key.
        """
        try:
            with open(file_path, "rb") as file:
                symmetric_key = file.read()
            return symmetric_key
        except Exception as e:
            raise RuntimeError(
                f"Error deserializing symmetric key from file '{file_path}': {e}"
            )
