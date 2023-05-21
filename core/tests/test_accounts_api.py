
from .fixtures import test_user
from fastapi.testclient import TestClient
from main import app
import pytest

@pytest.fixture(scope="session")
def test_client():
    # create a test client for the FastAPI application
    client = TestClient(app)

    # yield the test client
    yield client


def test_valid_data_login(test_client,test_user):
    # define test data
    data = {
        "email": "bigdeli.ali3@gmail.com",
        "password": "yourpassword"
    }

    # send a POST request to the login endpoint with the test data
    response = test_client.post("/accounts/api/v1/user/login/", json=data)
    
    # assert that the response status code is 200 OK
    assert response.status_code == 200 ,response.json()
    
    # asset that the response email is identical as the user 
    assert response.json()["email"] == test_user.email

    # assert that the response contains an access token
    assert "access_token" in response.json()
    
    
def test_invalid_data_login(test_client):
    # define test data
    data = {
        "email": "bigdeli.ali3@gmail.com",
        "password": "test_password"
    }

    # send a POST request to the login endpoint with the test data
    response = test_client.post("/accounts/api/v1/user/login/", json=data)
    
    # assert that the response status code is 401 OK
    assert response.status_code == 401 ,response.json()
