# from werkzeug.security import generate_password_hash
# print(generate_password_hash("moray001"))
# import secrets
# print(secrets.token_hex(32))
from werkzeug.security import generate_password_hash
with open('hash_output.txt', 'w') as f:
    f.write(generate_password_hash("@jackie001"))