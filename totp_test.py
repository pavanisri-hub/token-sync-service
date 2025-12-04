from totp_utils import generate_totp_code, verify_totp_code

# Use your decrypted seed:
hex_seed = "ccbc4b740622cc67bef2ef14d805e324627746e906860a6dea75d95d88e92f64"

# Generate OTP
code = generate_totp_code(hex_seed)
print("Generated OTP:", code)

# Verify OTP
print("OTP is valid:", verify_totp_code(hex_seed, code))
