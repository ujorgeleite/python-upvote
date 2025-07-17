from backend.database import SessionLocal
from backend.models import User
from backend.auth import get_password_hash

def seed_default_user():
    db = SessionLocal()
    username = "testuser"
    email = "testuser@example.com"
    password = "testpassword"
    if not db.query(User).filter(User.username == username).first():
        user = User(
            username=username,
            email=email,
            password_hash=get_password_hash(password)
        )
        db.add(user)
        db.commit()
        print(f"Inserted default user: {username} / {password}")
    else:
        print("Default user already exists.")
    db.close()

if __name__ == "__main__":
    seed_default_user() 