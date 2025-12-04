import os
import time
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from decrypt_seed import load_private_key, decrypt_seed
from totp_utils import generate_totp_code, verify_totp_code

app = FastAPI()

DATA_PATH = "data/seed.txt"


class SeedRequest(BaseModel):
    encrypted_seed: str


class VerifyRequest(BaseModel):
    code: str


@app.post("/decrypt-seed")
def decrypt_seed_endpoint(body: SeedRequest):

    # Load student's private key
    try:
        private_key = load_private_key("student_private.pem")
    except Exception:
        raise HTTPException(status_code=500, detail="Cannot load private key")

    # Attempt decryption
    try:
        seed = decrypt_seed(body.encrypted_seed, private_key)
    except Exception:
        raise HTTPException(status_code=500, detail="Decryption failed")

    # Save seed persistently
    os.makedirs("data", exist_ok=True)
    with open(DATA_PATH, "w") as f:
        f.write(seed)

    return {"status": "ok"}


@app.get("/generate-2fa")
def generate_2fa():

    # Ensure seed exists
    if not os.path.exists(DATA_PATH):
        raise HTTPException(status_code=500, detail="Seed not decrypted yet")

    # Read seed
    with open(DATA_PATH) as f:
        seed = f.read().strip()

    # Generate TOTP
    try:
        code = generate_totp_code(seed)
    except Exception:
        raise HTTPException(status_code=500, detail="Failed to generate code")

    # Calculate remaining validity (0–29 seconds)
    valid_for = 30 - (int(time.time()) % 30)

    return {"code": code, "valid_for": valid_for}



@app.post("/verify-2fa")
def verify_2fa(body: VerifyRequest):

    # Validate input
    if not body.code:
        raise HTTPException(status_code=400, detail="Missing code")

    # Ensure seed exists
    if not os.path.exists(DATA_PATH):
        raise HTTPException(status_code=500, detail="Seed not decrypted yet")

    # Load seed
    with open(DATA_PATH) as f:
        seed = f.read().strip()

    # Verify
    is_valid = verify_totp_code(seed, body.code)

    return {"valid": is_valid}
