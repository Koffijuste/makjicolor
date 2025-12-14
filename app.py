import os
from __init__ import create_app
from admin import init_admin

app = create_app()

app.secret_key = os.environ.get("SECRET_KEY")

init_admin(app)

if __name__ == "__main__":
    app.run(debug=True)