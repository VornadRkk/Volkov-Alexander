import os

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.asymmetric import padding  as asymmetric_padding
from cryptography.hazmat.primitives import hashes,serialization,padding
from cryptography.hazmat.backends import default_backend


from generates_key_hybrid_system import Key
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
            key_manager = Key()
            symmetric_key = key_manager.deserialize_symmetric_key(symmetric_key_path)
            public_key = key_manager.deserialize_asymmetric_key(public_key_path, is_private=False)
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
    
    def decrypt_symmetric_key(self, private_key_path: str, encrypted_symmetric_key: bytes) -> bytes:
        """
        Decrypt a symmetric key using a private RSA key.

        Args:
            private_key_path (str): Path to the file containing the private RSA key.
            encrypted_symmetric_key (bytes): Encrypted symmetric key.

        Returns:
            bytes: Decrypted symmetric key.
        """
        try:
            with open(private_key_path, "rb") as key_file:
                private_key = serialization.load_pem_private_key(
                    key_file.read(),
                    password=None,
                    backend=default_backend()
                )
            symmetric_key = private_key.decrypt(
                encrypted_symmetric_key,
                asymmetric_padding.OAEP(
                    mgf=asymmetric_padding.MGF1(algorithm=hashes.SHA256()),
                    algorithm=hashes.SHA256(),
                    label=None
                )
            )

            return symmetric_key
        except Exception as e:
            raise RuntimeError(f"Error decrypting symmetric key: {e}")

    def encrypt_text_symmetric_key(text: str, key_file_path: str, encrypted_text_path: str) -> None:
        """
        Encrypts text using a symmetric key and saves the encrypted text to a file.

        Args:
            text (str): The text to be encrypted.
            key_file_path (str): Path to the file containing the symmetric key.
            encrypted_text_path (str): Path to save the encrypted text.

        Returns:
            None
        """
        try:
            key_manager = Key()
            key = key_manager.deserialize_symmetric_key(key_file_path)
            iv = os.urandom(16)
            padder = padding.PKCS7(128).padder()
            padded_text = padder.update(text.encode("utf-8")) + padder.finalize()
            cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
            encryptor = cipher.encryptor()
            encrypted_text = encryptor.update(padded_text) + encryptor.finalize()
            file_manager = WorkFile()
            file_manager.write_bytes(encrypted_text_path, iv + encrypted_text)
            print(f"Text encrypted and saved to '{encrypted_text_path}'")
        except Exception as e:
            raise RuntimeError(f"Failed to encrypt text: {e}")
    
    def decrypt_text_symmetric(encrypted_text_path: str, symmetric_key_path: str, decrypted_text_path: str) -> None:
        """
        Decrypts encrypted text using a symmetric key and saves the decrypted text to a file.

        Args:
            encrypted_text_path (str): Path to the file containing the encrypted text.
            symmetric_key_path (str): Path to the file containing the symmetric key.
            decrypted_text_path (str): Path to save the decrypted text.

        Returns:
            None
        """
        try:
            key_manager = Key()
            key = key_manager.deserialize_symmetric_key(symmetric_key_path)
            
            file_manager = WorkFile()
            encrypted_data = file_manager.read_bytes(encrypted_text_path)
            iv = encrypted_data[:16]
            encrypted_text = encrypted_data[16:]
            
            cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
            decryptor = cipher.decryptor()
            decrypted_text = decryptor.update(encrypted_text) + decryptor.finalize()
            
            unpadder = padding.PKCS7(128).unpadder()
            unpadded_text = unpadder.update(decrypted_text) + unpadder.finalize()
            
            file_manager.write_text(decrypted_text_path, unpadded_text.decode("utf-8"))
            print(f"Text decrypted and saved to '{decrypted_text_path}'")
        except Exception as e:
            raise RuntimeError(f"Failed to decrypt text: {e}")