import pytest
import httpx

BASE_URL = "http://127.0.0.1:8000/api"

TEST_EMAIL = "nuevo.usuario@example.com"
TEST_NAME = "Usuario Prueba Flow"
TEST_PHONE = "3001234567"



@pytest.mark.asyncio
async def test_check_email_not_exists():
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{BASE_URL}/clients/check-email",
            json={"email": TEST_EMAIL}
        )
    
    assert response.status_code == 200
    data = response.json()
    assert data["exists"] is False
    assert data["client"] is None



@pytest.mark.asyncio
async def test_create_client():
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{BASE_URL}/clients",
            json={
                "name": TEST_NAME,
                "email": TEST_EMAIL,
                "phone": TEST_PHONE
            }
        )
    

    assert response.status_code in [201, 400]



@pytest.mark.asyncio
async def test_check_email_exists():
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{BASE_URL}/clients/check-email",
            json={"email": TEST_EMAIL}
        )
    
    assert response.status_code == 200
    data = response.json()
    assert data["exists"] is True
    assert data["client"]["email"] == TEST_EMAIL



@pytest.mark.asyncio
async def test_create_new_pet():
    payload = {
        "client_email": TEST_EMAIL,
        "pet_name": "MaxTest",
        "pet_species": "Perro"
    }
    async with httpx.AsyncClient() as client:
        response = await client.post(f"{BASE_URL}/pets", json=payload)
    
    assert response.status_code == 200
    data = response.json()
    assert "pet_id" in data



@pytest.mark.asyncio
async def test_find_existing_pet():
    payload = {
        "client_email": TEST_EMAIL,
        "pet_name": "MaxTest",
        "pet_species": "Perro"
    }
    async with httpx.AsyncClient() as client:
        response = await client.post(f"{BASE_URL}/pets", json=payload)
    
    assert response.status_code == 200
    data = response.json()
    assert data["is_new"] is False
    assert data["message"] == "Mascota existente recuperada con exito"



@pytest.mark.asyncio
async def test_invalid_pet_species():
    payload = {
        "client_email": TEST_EMAIL,
        "pet_name": "Lucas",
        "pet_species": "Loro" 
    }
    async with httpx.AsyncClient() as client:
        response = await client.post(f"{BASE_URL}/pets", json=payload)
    
    assert response.status_code == 422