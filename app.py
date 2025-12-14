import os
from admin import init_admin
from __init__ import create_app

app = create_app()

# 🔐 SECRET_KEY AVANT tout (sessions / admin)
app.secret_key = os.environ.get("SECRET_KEY")
if not app.secret_key:
    raise RuntimeError("❌ SECRET_KEY manquant")

# Init Flask-Admin (UNE seule fois)
init_admin(app)

if __name__ == "__main__":
    app.run()