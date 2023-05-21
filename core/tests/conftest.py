import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from core.database import Base
import os


@pytest.fixture(scope="session")
def test_db():
    # create a test database
    engine = create_engine(os.environ.get("DATABASE_URL"))

    # create the tables in the test database
    Base.metadata.create_all(bind=engine)

    # create a sessionmaker for the test database
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    # yield the sessionmaker
    yield SessionLocal

    # drop the tables in the test database
    Base.metadata.drop_all(bind=engine)