import os

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.ciphers import algorithms, Cipher, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from typing import Union



class Key:


    def __init__(self):
        pass

    def generate_symetric_key(self, key_length: int) -> bytes:
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
    
    def generate_assymetric_keys(self, key_length: int)->bytes:
        """
        Generate RSA key pair with a specified key length.

        Args:
            key_length (int): Length of the key in bits.

        Returns:
            Tuple[RSAPrivateKey, RSAPublicKey]: Private and public keys.
        """
        try:
            private_key = rsa.generate_private_key(
                public_exponent=65537,
                key_size=key_length,
            )
            public_key = private_key.public_key()
            return private_key, public_key
        except Exception as e:
            raise RuntimeError(f"Error generating RSA keys: {e}")
    
    def serialize_symmetric_key(self, symmetric_key: bytes, file_path: str) -> None:
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
            raise RuntimeError(f"Error serializing symmetric key to file '{file_path}': {e}")
    
    def deserialize_symmetric_key(self, file_path: str) -> bytes:
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
            raise RuntimeError(f"Error deserializing symmetric key from file '{file_path}': {e}")

    def serialize_asymmetric_key(self, key, file_path: str) -> None:
        """
        Serialize an asymmetric key to a file.

        Args:
            key: Asymmetric key object to be serialized.
            file_path (str): Path to the file.
        """
        try:
            with open(file_path, "wb") as file:
                serialized_key = key.private_bytes(
                    encoding=serialization.Encoding.PEM,
                    format=serialization.PrivateFormat.TraditionalOpenSSL,
                    encryption_algorithm=serialization.NoEncryption()
                ) if isinstance(key, rsa.RSAPrivateKey) else key.public_bytes(
                    encoding=serialization.Encoding.PEM,
                    format=serialization.PublicFormat.SubjectPublicKeyInfo
                )
                file.write(serialized_key)
        except Exception as e:
            raise RuntimeError(f"Error serializing key to file '{file_path}': {e}")

    def deserialize_asymmetric_key(self, file_path: str, is_private: bool) -> Union[RSAPrivateKey, RSAPublicKey]:
        """
        Deserialize an asymmetric key from a file.

        Args:
            file_path (str): Path to the file containing the serialized key.
            is_private (bool): Whether the key is private or public.

        Returns:
            RSAPrivateKey or RSAPublicKey: Deserialized key object.
        """
        try:
            with open(file_path, "rb") as file:
                key_data = file.read()
            if is_private:
                return serialization.load_pem_private_key(key_data, password=None, backend=default_backend())
            else:
                return serialization.load_pem_public_key(key_data, backend=default_backend())   
        except Exception as e:
            raise RuntimeError(f"Error deserializing key from file '{file_path}': {e}")
        
