import os
from app import app
from user_models import db

# 🔧 Make sure instance/ exists
os.makedirs(app.instance_path, exist_ok=True)

with app.app_context():
    print("📂 DB URI:", app.config["SQLALCHEMY_DATABASE_URI"])
    db.create_all()
    print("✅ users.db rebuilt successfully")