import time
import os
from totp_utils import generate_totp_code

SEED_PATH = "/data/seed.txt"
LOG_PATH = "/cron/last_code.txt"

def run():
    if not os.path.exists(SEED_PATH):
        print("Seed not found.")
        return

    with open(SEED_PATH) as f:
        seed = f.read().strip()

    code = generate_totp_code(seed)
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())

    os.makedirs("/cron", exist_ok=True)

    with open(LOG_PATH, "a") as log_file:
        log_file.write(f"{timestamp} - 2FA Code: {code}\n")

if __name__ == "__main__":
    run()
