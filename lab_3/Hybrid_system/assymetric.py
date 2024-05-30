from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.asymmetric import padding as crypto_padding
from cryptography.hazmat.primitives import hashes

from Hybrid_system.serialization_and_deserialization import Serealization
from Hybrid_system.work_with_json import WorkFile


class Assymetric:
    """
    A class for generating, serializing, and deserializing asymmetric keys (RSA).

    Attributes:
        None

    Methods:
        generate_assymetric_keys(key_length: int) -> Tuple[RSAPrivateKey, RSAPublicKey]:
            Generate RSA key pair with a specified key length.
        encrypt_symmetric_key_with_public_key(
            symmetric_key_path: str, public_key_path: str, encrypted_key_path: str
        ) -> None:
            Encrypts a symmetric key with a public RSA key and saves the encrypted key to a file.

        decrypt_symmetric_key(
            encrypted_key_path: str, private_key_path: str, decrypted_symmetric_key: str
        ) -> bytes:
            Decrypts a symmetric key using a private RSA key and saves the decrypted key to a file.
    """

    @staticmethod
    def generate_assymetric_keys() -> tuple[rsa.RSAPublicKey, rsa.RSAPrivateKey]:
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
                key_size=2048,
            )
            public_key = private_key.public_key()
            return public_key, private_key
        except Exception as e:
            raise RuntimeError(f"Error generating RSA keys: {e}")

    @staticmethod
    def encrypt_symmetric_key_with_public_key(
        symmetric_key_path: str, public_key_path: str, encrypted_key_path: str
    ) -> None:
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
            symmetric_key = Serealization.deserialize_symmetric_key(symmetric_key_path)
            public_key = Serealization.deserialize_asymmetric_public_key(
                public_key_path
            )
            encrypted_key = public_key.encrypt(
                symmetric_key,
                crypto_padding.OAEP(
                    mgf=crypto_padding.MGF1(algorithm=hashes.SHA256()),
                    algorithm=hashes.SHA256(),
                    label=None,
                ),
            )
            file_manager = WorkFile()
            file_manager.write_bytes_to_file(encrypted_key_path, encrypted_key)
            print(f"Symmetric key encrypted and saved to '{encrypted_key_path}'")
        except Exception as e:
            raise RuntimeError(f"Failed to encrypt symmetric key: {e}")

    @staticmethod
    def decrypt_symmetric_key(
        encrypted_key_path: str, private_key_path: str, decrypted_symmetric_key: str
    ) -> bytes:
        """
        Decrypt a symmetric key using a private RSA key.

        Args:
            private_key_path (str): Path to the file containing the private RSA key.
            encrypted_symmetric_key (bytes): Encrypted symmetric key.

        Returns:
            bytes: Decrypted symmetric key.
        """
        try:
            symmetric_key = Serealization.deserialize_symmetric_key(encrypted_key_path)
            private_key = Serealization.deserialize_asymmetric_private_key(
                private_key_path
            )
            decrypted_key = private_key.decrypt(
                symmetric_key,
                crypto_padding.OAEP(
                    mgf=crypto_padding.MGF1(algorithm=hashes.SHA256()),
                    algorithm=hashes.SHA256(),
                    label=None,
                ),
            )
            file_manager = WorkFile()
            file_manager.write_bytes_to_file(decrypted_symmetric_key, decrypted_key)
            print(f"Symmetric key decrypted and saved to '{decrypted_symmetric_key}'")
            return decrypted_key
        except Exception as e:
            raise RuntimeError(f"Error decrypting symmetric key: {e}")
