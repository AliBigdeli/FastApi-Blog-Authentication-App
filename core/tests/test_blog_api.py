from fastapi.testclient import TestClient
from main import app
import pytest


@pytest.fixture(scope="session")
def test_client():
    # create a test client for the FastAPI application
    client = TestClient(app)

    # yield the test client
    yield client


def test_non_auth_posts_list_res_200(test_client):
    # send a POST request to the login endpoint with the test data
    response = test_client.get("/blog/api/v1/post/")

    # assert that the response status code is 200 OK
    assert response.status_code == 200, response.json()


# def test_non_auth_post_detail_res_200(test_client, test_post):

#     # send a POST request to the login endpoint with the test data
#     response = test_client.get(f"/blog/api/v1/post/{test_post.id}/")

#     # assert that the response status code is 200 OK
#     assert response.status_code == 200, response.json()


def test_non_auth_post_detail_res_404(test_client):
    # send a POST request to the login endpoint with the test data
    response = test_client.get("/blog/api/v1/post/192/")

    # assert that the response status code is 200 OK
    assert response.status_code == 404, response.json()
