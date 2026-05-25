import bcrypt

print(bcrypt.hashpw("anibal2024".encode(), bcrypt.gensalt()).decode())