import base64
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes, serialization


def load_private_key(path: str):
    """Load student's private RSA key from PEM file."""
    with open(path, "rb") as f:
        return serialization.load_pem_private_key(
            f.read(),
            password=None
        )


def decrypt_seed(encrypted_seed_b64: str, private_key) -> str:
    """
    Decrypt base64-encoded encrypted seed using RSA/OAEP-SHA256
    Returns 64-character hex string.
    """

    # 1. Base64 decode to bytes
    encrypted_bytes = base64.b64decode(encrypted_seed_b64)

    # 2. RSA-OAEP decrypt
    decrypted_bytes = private_key.decrypt(
        encrypted_bytes,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    # 3. Convert decrypted bytes → string
    seed = decrypted_bytes.decode()

    # 4. Validate length = 64 hex chars
    if len(seed) != 64:
        raise ValueError("Seed must be 64 hex characters")

    if not all(c in "0123456789abcdef" for c in seed.lower()):
        raise ValueError("Seed is not valid hex")

    return seed
