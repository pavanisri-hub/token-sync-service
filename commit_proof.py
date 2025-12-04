import base64
import subprocess
from pathlib import Path
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding

def get_latest_commit_hash() -> str:
    """
    Run: git log -1 --format=%H
    and return the 40-character commit hash as a string.
    """
    output = subprocess.check_output(
        ["git", "log", "-1", "--format=%H"],
        text=True
    )
    commit_hash = output.strip()
    if len(commit_hash) != 40:
        raise ValueError(f"Unexpected commit hash length: {commit_hash}")
    return commit_hash

def load_private_key(path: Path):
    """
    Load student private key from PEM file.
    """
    with path.open("rb") as f:
        data = f.read()
    private_key = serialization.load_pem_private_key(
        data,
        password=None,
    )
    return private_key


def load_public_key(path: Path):
    """
    Load instructor public key from PEM file.
    """
    with path.open("rb") as f:
        data = f.read()
    public_key = serialization.load_pem_public_key(data)
    return public_key

def sign_message(message: str, private_key) -> bytes:
    """
    Sign a message using RSA-PSS with SHA-256.

    1. Encode commit hash as ASCII bytes
    2. Sign using RSA-PSS with:
       - MGF1(SHA-256)
       - salt_length = PSS.MAX_LENGTH
    """
    message_bytes = message.encode("utf-8") 

    signature = private_key.sign(
        message_bytes,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH,
        ),
        hashes.SHA256(),
    )
    return signature


def encrypt_with_public_key(data: bytes, public_key) -> bytes:
    """
    Encrypt data using RSA/OAEP with SHA-256.
    """
    ciphertext = public_key.encrypt(
        data,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None,
        ),
    )
    return ciphertext



def main():
    repo_root = Path(__file__).resolve().parent

    commit_hash = get_latest_commit_hash()
    print(f"Commit Hash: {commit_hash}")

    student_private_path = repo_root / "student_private.pem"
    private_key = load_private_key(student_private_path)

    signature = sign_message(commit_hash, private_key)

    instructor_public_path = repo_root / "instructor_public.pem"
    instructor_pub = load_public_key(instructor_public_path)

    encrypted_signature = encrypt_with_public_key(signature, instructor_pub)

    encrypted_b64 = base64.b64encode(encrypted_signature).decode("ascii")

    print("\nEncrypted Signature (Base64):")
    print(encrypted_b64)


if __name__ == "__main__":
    main()
