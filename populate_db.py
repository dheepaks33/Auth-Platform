from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from app.models import Base, User, Organisation, Role, Member
from app.database import engine

# Create a session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
db = SessionLocal()

def add_dummy_data():
    # Add Organisation
    org = Organisation(name="Test Org", status=1, personal=False, settings={}, created_at=1234567890, updated_at=1234567890)
    db.add(org)
    db.commit()

    # Add User
    user = User(email="test@example.com", password="hashed_password", profile={}, status=1, settings={}, created_at=1234567890, updated_at=1234567890)
    db.add(user)
    db.commit()

    # Add Role
    role = Role(name="Admin", description="Administrator role", org_id=1)
    db.add(role)
    db.commit()

    # Add Member
    member = Member(org_id=1, user_id=1, role_id=1, status=1, settings={}, created_at=1234567890, updated_at=1234567890)
    db.add(member)
    db.commit()

    print("Dummy data added!")

if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)  # Create tables
    add_dummy_data()
