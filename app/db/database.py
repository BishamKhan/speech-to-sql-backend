from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from dotenv import load_dotenv
import os

load_dotenv()

URL_DATABASE = os.getenv("DATABASE_URL")

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

