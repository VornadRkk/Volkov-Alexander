import os

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding

from Hybrid_system.work_with_json import WorkFile
from Hybrid_system.serialization_and_deserialization import Serealization


class Symetric:
    """
    A class for generating, serializing, and deserializing symmetric keys (3DES).

    Attributes:
        None

    Methods:
        generate_symmetric_key(key_length: int) -> bytes:
            Generate a 3DES key with a specified length.
        encrypt_text_symmetric_key(
            text_path: str, symmetric_path: str, encrypted_text_path: str
        ) -> bytes:
            Encrypts text using a symmetric key and saves the encrypted text to a file.

        decrypt_text_symmetric(
            encrypted_text_path: str, symmetric_key_path: str, decrypted_text_path: str
        ) -> str:
            Decrypts encrypted text using a symmetric key and saves the decrypted text to a file.
    """

    @staticmethod
    def generate_symmetric_key(key_length: int) -> bytes:
        """
        Генерирует ключ 3DES с указанной длиной.

        Аргументы:
            key_length (int): Длина ключа в битах (64, 128 или 192).

        Возвращает:
            bytes: Ключ 3DES.
        """
        while True:
            try:
                if key_length == 64:
                    return os.urandom(8) * 2
                elif key_length == 128:
                    return os.urandom(16)
                elif key_length == 192:
                    return os.urandom(24)
                else:
                    raise ValueError("The key length must be 64, 128, or 192 bits.")
            except ValueError as ve:
                print(ve)
                key_length = int(
                    input("Enter the correct key length (64, 128 or 192): ")
                )

    @staticmethod
    def encrypt_text_symmetric_key(
        text_path: str, symetric_path: str, encrypted_text_path: str
    ) -> bytes:
        """
        Encrypts text using a symmetric key and returns the encrypted text as bytes.

        Args:
            text (str): The text to be encrypted.
            key_file_path (str): Path to the file containing the symmetric key.
            encrypted_text_path (str): Path to save the encrypted text.

        Returns:
            bytes: The encrypted text.
        """
        try:
            key = Serealization.deserialize_symmetric_key(symetric_path)
            iv = os.urandom(8)
            file_manager = WorkFile()
            text = file_manager.read_text_file(text_path)
            padder = padding.PKCS7(128).padder()
            padded_text = padder.update(text.encode("utf-8")) + padder.finalize()
            cipher = Cipher(algorithms.TripleDES(key), modes.CBC(iv))
            encryptor = cipher.encryptor()
            encrypted_text = encryptor.update(padded_text) + encryptor.finalize()
            encrypted_bytes = iv + encrypted_text
            file_manager.write_bytes_to_file(encrypted_text_path, encrypted_bytes)
            print(f"Text encrypted and saved to '{encrypted_text_path}'")
            return encrypted_bytes
        except Exception as e:
            raise RuntimeError(f"Failed to encrypt text: {e}")

    @staticmethod
    def decrypt_text_symmetric(
        encrypted_text_path: str, symmetric_key_path: str, decrypted_text_path: str
    ) -> str:
        """
        Decrypts encrypted text using a symmetric key and returns the decrypted text.

        Args:
            encrypted_text_path (str): Path to the file containing the encrypted text.
            symmetric_key_path (str): Path to the file containing the symmetric key.
            decrypted_text_path (str): Path to save the decrypted text.

        Returns:
            str: The decrypted text.
        """
        try:
            key = Serealization.deserialize_symmetric_key(symmetric_key_path)
            file_manager = WorkFile()
            encrypted_data = file_manager.read_key_bytes(encrypted_text_path)
            iv = encrypted_data[:8]
            encrypted_text = encrypted_data[8:]
            cipher = Cipher(algorithms.TripleDES(key), modes.CBC(iv))
            decryptor = cipher.decryptor()
            decrypted_text = decryptor.update(encrypted_text) + decryptor.finalize()
            unpadder = padding.PKCS7(128).unpadder()
            unpadded_text = unpadder.update(decrypted_text) + unpadder.finalize()
            decrypted_str = unpadded_text.decode("utf-8")
            print(decrypted_str)
            file_manager.write_text_file(decrypted_str, decrypted_text_path)
            print(f"Text decrypted and saved to '{decrypted_text_path}'")
            return decrypted_str
        except Exception as e:
            raise RuntimeError(f"Failed to decrypt text: {e}")
