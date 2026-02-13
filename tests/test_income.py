def test_create_income(client, auth_headers):
    response = client.post(
        "/income/",
        json={
            "amount": 3000.0,
            "source": "Salary",
            "type": "transfer",
            "date": "2024-02-10T12:00:00"
        },
        headers=auth_headers
    )
    assert response.status_code == 200
    data = response.json()
    assert data["data"]["amount"] == 3000.0
    assert data["data"]["source"] == "Salary"

def test_get_incomes(client, auth_headers):
    # Create two income entries
    client.post(
        "/income/",
        json={"amount": 1000.0, "source": "Freelance"},
        headers=auth_headers
    )
    client.post(
        "/income/",
        json={"amount": 500.0, "source": "Gift"},
        headers=auth_headers
    )

    response = client.get("/income/", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()["data"]
    assert len(data) >= 2
    sources = [item["source"] for item in data]
    assert "Freelance" in sources
    assert "Gift" in sources
