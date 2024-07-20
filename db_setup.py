from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///pro_finder.db")
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
Session = sessionmaker(bind=engine)

def setup_db():
    session = Session()
    # Create tables if they don't exist
    session.execute(text('''
        CREATE TABLE IF NOT EXISTS contractors (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            number TEXT NOT NULL,
            city TEXT NOT NULL,
            service TEXT NOT NULL,
            feedback TEXT
        )
    '''))
    session.execute(text('''
        CREATE TABLE IF NOT EXISTS service_suggestions (
            id INTEGER PRIMARY KEY,
            suggested_service TEXT NOT NULL UNIQUE,
            name TEXT NOT NULL,
            number TEXT NOT NULL,
            city TEXT NOT NULL,
            price REAL NOT NULL,
            feedback TEXT
        )
    '''))
    session.execute(text('''
        CREATE TABLE IF NOT EXISTS services (
            id INTEGER PRIMARY KEY,
            service_name TEXT NOT NULL UNIQUE
        )
    '''))
    session.commit()
    session.close()
