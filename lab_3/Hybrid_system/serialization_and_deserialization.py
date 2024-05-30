from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.serialization import (
    load_pem_public_key,
    load_pem_private_key,
)


class Serealization:
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

    @staticmethod
    def serialize_private_key(key: rsa.RSAPrivateKey, file_path: str) -> None:
        """
        Serialize a private key to a file.

        Args:
            key: Private key object to be serialized.
            file_path (str): Path to the file.
        """
        try:
            with open(file_path, "wb") as file:
                serialized_key = key.private_bytes(
                    encoding=serialization.Encoding.PEM,
                    format=serialization.PrivateFormat.TraditionalOpenSSL,
                    encryption_algorithm=serialization.NoEncryption(),
                )
                file.write(serialized_key)
        except Exception as e:
            raise RuntimeError(
                f"Error serializing private key to file '{file_path}': {e}"
            )
    @staticmethod
    def serialize_public_key(key: rsa.RSAPublicKey, file_path: str) -> None:
        """
        Serialize a public key to a file.
        Args:
            key: Public key object to be serialized.
            file_path (str): Path to the file.
        """
        try:
            with open(file_path, "wb") as file:
                serialized_key = key.public_bytes(
                    encoding=serialization.Encoding.PEM,
                    format=serialization.PublicFormat.SubjectPublicKeyInfo,
                )
                file.write(serialized_key)
        except Exception as e:
            raise RuntimeError(
                f"Error serializing public key to file '{file_path}': {e}"
            )

    @staticmethod
    def deserialize_asymmetric_public_key(file_path: str) -> rsa.RSAPublicKey:
        """
        Deserialize an asymmetric key from a file.

        Args:
            file_path (str): Path to the file containing the serialized key.
            is_private (bool): Whether the key is private or public.

        Returns:
            RSAPrivateKey or RSAPublicKey: Deserialized key object.
        """
        try:
            with open(file_path, "rb") as pem_in:
                public_bytes = pem_in.read()
            d_public_key = load_pem_public_key(public_bytes)
            return d_public_key
        except Exception as e:
            raise RuntimeError(f"Error deserializing key from file '{file_path}': {e}")

    @staticmethod
    def deserialize_asymmetric_private_key(file_path: str) -> rsa.RSAPrivateKey:
        """
        Deserialize an asymmetric key from a file.

        Args:
            file_path (str): Path to the file containing the serialized key.
            is_private (bool): Whether the key is private or public.

        Returns:
            RSAPrivateKey or RSAPublicKey: Deserialized key object.
        """
        try:
            with open(file_path, "rb") as pem_in:
                private_bytes = pem_in.read()
            d_private_key = load_pem_private_key(
                private_bytes,
                password=None,
            )
            return d_private_key
        except Exception as e:
            raise RuntimeError(f"Error deserializing key from file '{file_path}': {e}")
