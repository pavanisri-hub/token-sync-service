import os
from datetime import datetime, timezone
from totp_utils import generate_totp_code, hex_to_base32

SEED_FILE = "/data/seed.txt"

def read_seed():
    if not os.path.exists(SEED_FILE):
        print("Seed file not found")
        return None

    with open(SEED_FILE, "r") as f:
        seed_hex = f.read().strip()

    if len(seed_hex) != 64:
        print("Invalid seed in file")
        return None

    return seed_hex

def main():
    seed_hex = read_seed()
    if seed_hex is None:
        return

    seed_b32 = hex_to_base32(seed_hex)
    code = generate_totp_code(seed_b32)

    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")

    print(f"{timestamp} - 2FA Code: {code}")

if __name__ == "__main__":
    main()
