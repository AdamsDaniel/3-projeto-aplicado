from sqlmodel import Session, select
from projeto_aplicado.ext.database.db import engine
from projeto_aplicado.resources.user.model import User, UserRole
from projeto_aplicado.auth.password import get_password_hash

def create_admin():
    with Session(engine) as session:
        existing = session.exec(select(User).where(User.username == "admin")).first()
        if existing:
            print("Admin already exists")
            return
            
        admin = User(
            username="admin",
            email="admin@foodtruck.com",
            password=get_password_hash("admin123"),
            full_name="Admin",
            role=UserRole.ADMIN
        )
        session.add(admin)
        session.commit()
        print("Admin user created successfully")

if __name__ == "__main__":
    create_admin()
