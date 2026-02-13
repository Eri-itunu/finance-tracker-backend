## 1. Automated Tests (Recommended)
We use `pytest` for automated testing. Integration tests use a temporary SQLite database.

**Run all tests:**
```bash
python -m pytest tests/
```

**Run with coverage report:**
```bash
python -m pytest tests/ --cov=app
```

## 2. Verify Manually
Server should be running at: `http://127.0.0.1:8000`

## 2. Interactive Documentation (Swagger UI)
The easiest way to test is to open your browser to:
[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

1.  Click **POST /users/** to create a user.
    -   Click "Try it out".
    -   Enter JSON: `{"email": "test@example.com", "password": "password123", "first_name": "Test", "last_name": "User"}`.
    -   Click "Execute".
2.  Click **POST /token** to login.
    -   Click "Try it out".
    -   Enter `username` (email) and `password`.
    -   Click "Execute".
    -   Copy the `access_token` from the response.
3.  Click **Authorize** (top right) and paste the token to test protected endpoints.

## 3. Command Line (cURL)
**Create User:**
```bash
curl -X 'POST' \
  'http://127.0.0.1:8000/users/' \
  -H 'Content-Type: application/json' \
  -d '{
  "email": "user@example.com",
  "password": "secretpassword",
  "first_name": "John",
  "last_name": "Doe"
}'
```

**Login:**
```bash
curl -X 'POST' \
  'http://127.0.0.1:8000/token' \
  -H 'Content-Type: application/x-www-form-urlencoded' \
  -d 'username=user@example.com&password=secretpassword'
```
