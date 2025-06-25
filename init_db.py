from app import app
from user_models import db, User

with app.app_context():
    print("📂 DB URI:", app.config["SQLALCHEMY_DATABASE_URI"])
    print("🔧 Creating all tables...")
    db.create_all()
    print("✅ Done! Tables created.")