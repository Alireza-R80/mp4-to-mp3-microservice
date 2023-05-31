from config import settings
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Define the connection string for MySQL
DATABASE_URL = f"mysql+mysqldb://{settings.mysql_user}:{settings.mysql_password}@{settings.mysql_host}/{settings.mysql_database}"

# Create the SQLAlchemy engine
engine = create_engine(DATABASE_URL)

# Create a session class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create the base class for your models
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
