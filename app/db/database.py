from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from dotenv import load_dotenv
import os
from pathlib import Path

# Ensure the .env in the app folder is loaded even when running from project root
BASE_DIR = Path(__file__).resolve().parent.parent
DOTENV_PATH = BASE_DIR / '.env'
if DOTENV_PATH.exists():
    load_dotenv(DOTENV_PATH)
else:
    # fallback to default behavior
    load_dotenv()

URL_DATABASE = os.getenv("DATABASE_URL")
if not URL_DATABASE:
    raise RuntimeError(f"DATABASE_URL not set. Checked {DOTENV_PATH}")

engine = create_engine(URL_DATABASE, pool_size= 2, max_overflow= 5,

    connect_args={"connect_timeout": 5},  # fail fast if DB down
    echo=True  # optional: debug info
)

Sessionlocal = sessionmaker(autocommit=False, autoflush=False, bind= engine)

Base = declarative_base()


# DB dependency
def get_db():
    db = Sessionlocal()
    try:
        yield db
    finally:
        db.close()

