from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_autenticacao():
    response = client.post("/token", params={"usuario": "user", "senha": "pass"})
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_dados_producao():
    token = client.post("/token", params={"usuario": "user", "senha": "pass"}).json()["access_token"]
    response = client.get("/dados/producao?ano=2020", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert "dados" in response.json()