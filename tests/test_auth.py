def test_create_user(client):
    response = client.post(
        "/register",
        json={
            "email": "newuser@example.com",
            "password": "newpassword123",
            "first_name": "New",
            "last_name": "User",
            "default_currency": "USD"
        }
    )
    assert response.status_code == 201
    data = response.json()
    assert data["data"]["user"]["email"] == "newuser@example.com"
    assert "id" in data["data"]["user"]

def test_login_success(client, test_user):
    response = client.post(
        "/login",
        json={"email": test_user.email, "password": "password123"}
    )
    assert response.status_code == 200
    assert "access_token" in response.json()["data"]

def test_login_failure(client, test_user):
    response = client.post(
        "/login",
        json={"email": test_user.email, "password": "wrongpassword"}
    )
    assert response.status_code == 401
