"""
Database initialization script
Creates all tables and optionally seeds with sample data
"""
import sys
sys.path.append('..')

from app.models.database import Base
from app.db.session import engine
from app.db.config import settings

def init_database():
    """Create all database tables"""
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("✓ Database tables created successfully!")

def seed_sample_data():
    """Seed database with sample data for testing"""
    from app.db.session import SessionLocal
    from app.models.database import User, MemoryBranch, StoryBranchType

    db = SessionLocal()

    try:
        # Create sample user
        sample_user = User(
            name="Sample Grandparent",
            email="sample@example.com",
            phone_number="+1234567890"
        )
        db.add(sample_user)
        db.commit()
        db.refresh(sample_user)

        # Create sample memory branches
        branches = [
            MemoryBranch(
                user_id=sample_user.id,
                branch_type=StoryBranchType.CHILDHOOD,
                title="Growing Up in the 1950s",
                description="Memories from my childhood"
            ),
            MemoryBranch(
                user_id=sample_user.id,
                branch_type=StoryBranchType.CAREER,
                title="My Teaching Career",
                description="40 years in education"
            ),
            MemoryBranch(
                user_id=sample_user.id,
                branch_type=StoryBranchType.FAMILY,
                title="Family Moments",
                description="Special times with family"
            )
        ]

        for branch in branches:
            db.add(branch)

        db.commit()
        print("✓ Sample data seeded successfully!")

    except Exception as e:
        print(f"Error seeding data: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    print("Story AI - Database Initialization")
    print(f"Database URL: {settings.DATABASE_URL}")
    print()

    init_database()

    # Ask if user wants to seed sample data
    response = input("\nWould you like to seed sample data? (y/n): ")
    if response.lower() == 'y':
        seed_sample_data()

    print("\n✓ Database initialization complete!")
