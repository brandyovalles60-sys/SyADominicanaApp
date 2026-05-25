import bcrypt

password = "12345".encode()
hash = bcrypt.hashpw(password, bcrypt.gensalt())

print(hash.decode())