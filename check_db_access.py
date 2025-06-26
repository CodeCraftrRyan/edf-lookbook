import os
from app import app
from user_models import db, User

print("➡️ Current working directory:", os.getcwd())
print("📁 Does 'instance/' folder exist?", os.path.exists("instance"))
print("📄 Does 'instance/users.db' exist?", os.path.exists("instance/users.db"))
print("🔐 Permissions on 'instance/users.db':")
os.system("ls -l instance/users.db")

with app.app_context():
    try:
        print("🔍 Trying to query User table...")
        user = User.query.first()
        print("✅ Success! User:", user)
    except Exception as e:
        print("❌ FAILED to access DB:")
        print(e)
        