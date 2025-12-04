from decrypt_seed import load_private_key, decrypt_seed

# Load private key
private_key = load_private_key("student_private.pem")

# Read encrypted seed
with open("encrypted_seed.txt") as f:
    encrypted_seed = f.read().strip()

# Decrypt it
seed = decrypt_seed(encrypted_seed, private_key)

print("Decrypted Seed:", seed)
