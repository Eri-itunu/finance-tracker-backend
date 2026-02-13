from datetime import date, timedelta

def test_create_spending(client, auth_headers):
    # First create a category
    cat_response = client.post(
        "/categories/",
        json={"category_name": "Food", "is_deleted": False},
        headers=auth_headers
    )
    category_id = cat_response.json()["data"]["id"]

    # Create spending
    response = client.post(
        "/spending/",
        json={
            "amount": 50.0,
            "notes": "Fast food",
            "item_name": "Burger",
            "category_id": category_id,
            "date": str(date.today()),
            "is_deleted": False
        },
        headers=auth_headers
    )
    assert response.status_code == 200
    assert response.json()["data"]["amount"] == 50.0

def test_get_spendings_filter(client, auth_headers):
    # Create a transaction for yesterday and today
    today = date.today()
    yesterday = today - timedelta(days=1)
    
    # Yesterday
    client.post(
        "/spending/",
        json={"amount": 10.0, "item_name": "Old", "date": str(yesterday)},
        headers=auth_headers
    )
    # Today
    client.post(
        "/spending/",
        json={"amount": 20.0, "item_name": "New", "date": str(today)},
        headers=auth_headers
    )

    # Filter for today only
    response = client.get(
        f"/spending/?start_date={today}&end_date={today}",
        headers=auth_headers
    )
    assert response.status_code == 200
    spendings = response.json()["data"]
    assert len(spendings) == 1
    assert spendings[0]["item_name"] == "New"

def test_invalid_date_range(client, auth_headers):
    today = date.today()
    tomorrow = today + timedelta(days=1)
    
    # start_date > end_date should fail
    response = client.get(
        f"/spending/?start_date={tomorrow}&end_date={today}",
        headers=auth_headers
    )
    assert response.status_code == 400
    assert "start_date cannot be after end_date" in response.json()["detail"]
