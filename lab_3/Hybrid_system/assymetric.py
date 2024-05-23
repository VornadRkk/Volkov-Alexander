from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.serialization import load_pem_public_key, load_pem_private_key



class Assymetric:

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
    
    def serialize_private_key(key, file_path: str) -> None:
            
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
                    encryption_algorithm=serialization.NoEncryption()
                )
                file.write(serialized_key)
        except Exception as e:
            raise RuntimeError(f"Error serializing private key to file '{file_path}': {e}")

    def serialize_public_key(key, file_path: str) -> None:
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
                    format=serialization.PublicFormat.SubjectPublicKeyInfo
                )
                file.write(serialized_key)
        except Exception as e:
            raise RuntimeError(f"Error serializing public key to file '{file_path}': {e}")
    
    def deserialize_asymmetric_public_key(self, file_path: str) -> rsa.RSAPublicKey:
        """
        Deserialize an asymmetric key from a file.

        Args:
            file_path (str): Path to the file containing the serialized key.
            is_private (bool): Whether the key is private or public.

        Returns:
            RSAPrivateKey or RSAPublicKey: Deserialized key object.
        """
        try:
            with open(file_path, 'rb') as pem_in:
                    public_bytes = pem_in.read()
            d_public_key = load_pem_public_key(public_bytes)
            return d_public_key
        except Exception as e:
            raise RuntimeError(f"Error deserializing key from file '{file_path}': {e}")
    
    def deserialize_asymmetric_private_key(self, file_path: str) -> rsa.RSAPrivateKey:
        """
        Deserialize an asymmetric key from a file.

        Args:
            file_path (str): Path to the file containing the serialized key.
            is_private (bool): Whether the key is private or public.

        Returns:
            RSAPrivateKey or RSAPublicKey: Deserialized key object.
        """
        try:
            with open(file_path, 'rb') as pem_in:
                    private_bytes  = pem_in.read()
            d_private_key = load_pem_private_key(private_bytes,password=None,)
            return d_private_key
        except Exception as e:
            raise RuntimeError(f"Error deserializing key from file '{file_path}': {e}")
        
