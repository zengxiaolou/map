from main import app

with app.test_client() as client:
    response = client.get("/hello")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}