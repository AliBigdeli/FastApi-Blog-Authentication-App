import pytest
from accounts.models import UserModel
import bcrypt


def generate_hashed_password(password):
    encoded_password = password.encode("utf-8")
    hashed_password = bcrypt.hashpw(encoded_password, bcrypt.gensalt())
    return hashed_password.decode("utf-8")


@pytest.fixture(scope="session")
def test_user(test_db):
    # create a test user
    user = UserModel(
        email="bigdeli.ali3@gmail.com",
        password=generate_hashed_password("yourpassword"),
    )

    # add the user to the test database
    db = test_db()
    db.add(user)
    db.commit()
    db.refresh(user)

    # yield the user object
    yield user

    # delete the user from the database
    db.delete(user)
    db.commit()
