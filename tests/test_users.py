# Test user-related functionality
from fastapi.testclient import TestClient
from app.main import app

# app = FastAPI()
client = TestClient(app)

### Test Cases
def test_create_user():
    response = client.post("/api/users", json={"email": "user1@gmail.com", "name": "User One"})
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "user1@gmail.com"
    assert data["name"] == "User One"

def test_create_user2():
    response = client.post("/api/users", json={"email": "user2@gmail.com", "name": "User Two"})
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "user2@gmail.com"
    assert data["name"] == "User Two"

def test_create_user3():
    response = client.post("/api/users", json={"email": "user3@gmail.com", "name": "User Three"})
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "user3@gmail.com"
    assert data["name"] == "User Three"

def test_create_user4():
    response = client.post("/api/users", json={"email": "user4@gmail.com", "name": "User Four"})
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "user4@gmail.com"
    assert data["name"] == "User Four"

def test_get_users():
    response = client.get("/api/users")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0  # Assuming at least one user exists

def test_get_user_by_email():
    response = client.post("/api/users/byEmail", json={"email": "user1@gmail.com"})
    assert response.status_code == 200  
    data = response.json()
    assert data["email"] == "user1@gmail.com"

def test_get_user_by_email_not_found():
    response = client.post("/api/users/byEmail", json={"email": "user2@gmail.com"})
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "User not found"

def test_create_user_invalid_email():
    response = client.post("/api/users", json={"email": "invalid-email", "name": "Invalid User"})
    assert response.status_code == 422  # Unprocessable Entity for invalid email format
    data = response.json()
    assert "email" in data["detail"][0]["loc"]  # Check if email validation error is present

def test_create_user_missing_fields():
    response = client.post("/api/users", json={"email": "user2@gmail.com"})
    assert response.status_code == 422 # Unprocessable Entity for missing name field
    data = response.json()
    assert "name" in data["detail"][0]["loc"]  # Check if name validation error is present


def test_create_user_duplicate_email():
    response = client.post("/api/users", json={"email": "user1@gmail.com", "name": "User One Duplicate"})
    assert response.status_code == 400  # Bad Request for duplicate email
    assert response.json() == {"detail": "User with this email already exists"}

def test_create_user_empty_email():
    response = client.post("/api/users", json={"email": "", "name": "Empty Email User"})
    assert response.status_code == 422  # Unprocessable Entity for empty email
    data = response.json()
    assert "email" in data["detail"][0]["loc"]  # Check if email validation error is present

def test_create_user_empty_name():
    response = client.post("/api/users", json={"email": "user1@gmail.com", "name": ""})
    assert response.status_code == 400 # Bad Request for empty name
    assert response.json() == {"detail": "Email and name are required"}
