def test_create_savings_goal(client, auth_headers):
    response = client.post(
        "/savings/",
        json={
            "goal_name": "New Car",
            "target_amount": 20000.0,
            "deadline": "2025-12-31T23:59:59"
        },
        headers=auth_headers
    )
    assert response.status_code == 200
    data = response.json()
    assert data["data"]["goal_name"] == "New Car"
    assert data["data"]["target_amount"] == 20000.0

def test_create_savings_contribution(client, auth_headers):
    # 1. Create a goal first
    goal_resp = client.post(
        "/savings/",
        json={"goal_name": "Emergency Fund", "target_amount": 1000.0},
        headers=auth_headers
    )
    goal_id = goal_resp.json()["data"]["id"]

    # 2. Add contribution
    response = client.post(
        f"/savings/{goal_id}/contributions/",
        json={"amount": 100.0, "date": "2024-02-10T15:00:00"},
        headers=auth_headers
    )
    assert response.status_code == 200
    data = response.json()
    assert data["data"]["amount"] == 100.0
    assert data["data"]["goal_id"] == goal_id

def test_get_savings_goals(client, auth_headers):
    client.post(
        "/savings/",
        json={"goal_name": "Travel", "target_amount": 500.0},
        headers=auth_headers
    )
    
    response = client.get("/savings/", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()["data"]
    assert len(data) >= 1
    assert any(g["goal_name"] == "Travel" for g in data)
