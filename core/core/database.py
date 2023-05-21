from sqlalchemy import create_engine
# from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker,declarative_base
from core.config import settings

SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.PGDB_USERNAME}:{settings.PGDB_PASSWORD}@{settings.PGDB_HOSTNAME}:{settings.PGDB_PORT}/{settings.PGDB_DBNAME}"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        

def create_db():
    return Base.metadata.create_all(bind=engine)