from werkzeug.security import generate_password_hash, check_password_hash

# Générer le hash
password = "Bonheur!78@"
hashed = generate_password_hash(password)  # par défaut pbkdf2:sha256
print(hashed)
