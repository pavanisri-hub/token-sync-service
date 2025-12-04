import base64
import pyotp


def hex_to_base32(hex_seed: str) -> str:
    """Convert 64-char hex seed → base32 (TOTP compatible)."""
    seed_bytes = bytes.fromhex(hex_seed)   # hex → bytes
    base32_seed = base64.b32encode(seed_bytes).decode("utf-8")  # bytes → base32 string
    return base32_seed


def generate_totp_code(hex_seed: str) -> str:
    """Generate current 6-digit TOTP code using SHA-1 & 30-sec interval."""

    base32_seed = hex_to_base32(hex_seed)

    totp = pyotp.TOTP(base32_seed, digits=6, interval=30)  # SHA-1 is default

    return totp.now()   # returns "123456"


def verify_totp_code(hex_seed: str, code: str, valid_window: int = 1) -> bool:
    """Verify TOTP code with ±30 sec tolerance (1 time step)."""

    base32_seed = hex_to_base32(hex_seed)

    totp = pyotp.TOTP(base32_seed, digits=6, interval=30)

    # valid_window=1 → checks previous, current, next time window
    return totp.verify(code, valid_window=valid_window)
