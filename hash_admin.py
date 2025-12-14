from werkzeug.security import generate_password_hash

password = "Bonheur!78@"

hash_ = generate_password_hash(
    password,
    method="pbkdf2:sha256",
    salt_length=16
)

print(hash_)
