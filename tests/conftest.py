import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient
import os

# Import our app parts
from app.database import Base, get_db
from app.main import app
from app.models import User

# Use a separate SQLite database for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="session", autouse=True)
def setup_database():
    # Create the tables
    Base.metadata.create_all(bind=engine)
    yield
    # Drop tables after session
    Base.metadata.drop_all(bind=engine)
    # Delete the test database file
    if os.path.exists("test.db"):
        os.remove("test.db")

@pytest.fixture
def db():
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)
    
    yield session
    
    session.close()
    transaction.rollback()
    connection.close()

@pytest.fixture
def client(db):
    def override_get_db():
        try:
            yield db
        finally:
            pass
            
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()

@pytest.fixture
def test_user(db):
    # Helper to create a user for tests
    from app.crud import get_password_hash
    user = User(
        email="testuser@example.com",
        password=get_password_hash("password123"),
        first_name="Test",
        last_name="User"
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@pytest.fixture
def auth_headers(client, test_user):
    # Helper to get auth headers for protected endpoints
    response = client.post(
        "/login",
        json={"email": test_user.email, "password": "password123"}
    )
    token = response.json()["data"]["access_token"]
    return {"Authorization": f"Bearer {token}"}
