import os

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.asymmetric import padding  as asymmetric_padding
from cryptography.hazmat.primitives import hashes,serialization,padding
from cryptography.hazmat.backends import default_backend


from Hybrid_system.assymetric import Assymetric
from Hybrid_system.symetric import Symetric
from work_with_json import WorkFile

class Encrypt:
    def encrypt_symmetric_key_with_public_key(symmetric_key_path: str, public_key_path: str, encrypted_key_path: str) -> None:
        """
        Encrypts a symmetric key with a public RSA key and saves the encrypted key to a file.

        Args:
            symmetric_key_path (str): Path to the file containing the symmetric key.
            public_key_path (str): Path to the file containing the RSA public key.
            encrypted_key_path (str): Path to save the encrypted symmetric key.

        Returns:
            None
        """
        try:
            symmetric_key = Symetric.deserialize_symmetric_key(symmetric_key_path)
            public_key = Assymetric.deserialize_asymmetric_public_key(public_key_path)
            encrypted_key = public_key.encrypt(
                symmetric_key,
                padding.OAEP(
                    mgf=padding.MGF1(algorithm=hashes.SHA256()),
                    algorithm=hashes.SHA256(),
                    label=None
                )
            )
            file_manager = WorkFile()
            file_manager.write_bytes(encrypted_key_path, encrypted_key)

            print(f"Symmetric key encrypted and saved to '{encrypted_key_path}'")
        except Exception as e:
            raise RuntimeError(f"Failed to encrypt symmetric key: {e}")
    
    def decrypt_symmetric_key(self,encrypted_key_path:str, private_key_path: str, encrypted_symmetric_key: bytes) -> bytes:
        """
        Decrypt a symmetric key using a private RSA key.

        Args:
            private_key_path (str): Path to the file containing the private RSA key.
            encrypted_symmetric_key (bytes): Encrypted symmetric key.

        Returns:
            bytes: Decrypted symmetric key.
        """
        try:
           symmetric_key = Symetric.deserialize_symmetric_key(encrypted_key_path)
           private_key = Assymetric.deserialize_asymmetric_private_key(private_key_path)
           decrypted_key = private_key.encrypt(
                symmetric_key,
                padding.OAEP(
                    mgf=padding.MGF1(algorithm=hashes.SHA256()),
                    algorithm=hashes.SHA256(),
                    label=None
                )
            )
           return decrypted_key
        except Exception as e:
            raise RuntimeError(f"Error decrypting symmetric key: {e}")

    def encrypt_text_symmetric_key(text: str, symetric_path: str, encrypted_text_path: str) -> bytes:
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
            key = Symetric.deserialize_symmetric_key(symetric_path)
            iv = os.urandom(16)
            padder = padding.PKCS7(128).padder()
            padded_text = padder.update(text.encode("utf-8")) + padder.finalize()
            cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
            encryptor = cipher.encryptor()
            encrypted_text = encryptor.update(padded_text) + encryptor.finalize()
            encrypted_bytes = iv + encrypted_text
            file_manager = WorkFile()
            file_manager.write_bytes(encrypted_text_path, encrypted_bytes)
            print(f"Text encrypted and saved to '{encrypted_text_path}'")
            return encrypted_bytes
        except Exception as e:
            raise RuntimeError(f"Failed to encrypt text: {e}")
        
    def decrypt_text_symmetric(encrypted_text_path: str, symmetric_key_path: str, decrypted_text_path: str) -> str:
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
            key = Symetric.deserialize_symmetric_key(symmetric_key_path)
            file_manager = WorkFile()
            encrypted_data = file_manager.read_bytes(encrypted_text_path)
            iv = encrypted_data[:16]
            encrypted_text = encrypted_data[16:]
            cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
            decryptor = cipher.decryptor()
            decrypted_text = decryptor.update(encrypted_text) + decryptor.finalize()
            unpadder = padding.PKCS7(128).unpadder()
            unpadded_text = unpadder.update(decrypted_text) + unpadder.finalize()
            decrypted_str = unpadded_text.decode("utf-8")
            file_manager.write_text(decrypted_text_path, decrypted_str)
            print(f"Text decrypted and saved to '{decrypted_text_path}'")
            return decrypted_str
        except Exception as e:
            raise RuntimeError(f"Failed to decrypt text: {e}")