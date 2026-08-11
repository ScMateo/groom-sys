import pytest
import httpx
from app.core.database import SessionLocal
from app.models.admin import AdminModel

BASE_URL = "http://127.0.0.1:8000/api/admin"

@pytest.fixture(autouse=True)
def setup_admin_user():
    """Crea un usuario administrador de prueba si no existe y cierra la sesión."""
    db = SessionLocal()
    try:
        admin = db.query(AdminModel).filter(AdminModel.username == "admin_test").first()
        if not admin:
            admin = AdminModel(username="admin_test", password_hash="secret123")
            db.add(admin)
            db.commit()
    finally:
        db.close()

@pytest.mark.asyncio
async def test_admin_login_success():
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.post(
            f"{BASE_URL}/login",
            json={"username": "admin_test", "password": "secret123"}
        )
    assert response.status_code == 200
    assert response.json()["authenticated"] is True

@pytest.mark.asyncio
async def test_admin_login_invalid():
    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.post(
            f"{BASE_URL}/login",
            json={"username": "admin_test", "password": "wrongpassword"}
        )
    assert response.status_code == 401
    assert response.json()["detail"] == "Informacion de acceso invalida"

@pytest.mark.asyncio
async def test_get_weekly_appointments():
    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.get(f"{BASE_URL}/weekly-appointments")
    assert response.status_code == 200
    data = response.json()
    assert "appointments" in data