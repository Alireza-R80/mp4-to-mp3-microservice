from database import Base
from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.orm import Session


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    admin = Column(Boolean, server_default="FALSE")

    def create(self, db: Session):
        db.add(self)
        db.commit()
        db.refresh(self)
