import asyncio
import httpx
import pytest

BASE_URL = "http://127.0.0.1:8000/api/appointments"


VALID_PET_ID = "41c513e9-dac5-4350-a862-49980ca2a773"
INVALID_PET_ID = "00000000-0000-0000-0000-000000000000"



@pytest.mark.asyncio
async def test_get_availability():
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{BASE_URL}/availability?date=2026-08-20")
        
    assert response.status_code == 200
    data = response.json()
    assert "slots" in data
    assert len(data["slots"]) > 0



@pytest.mark.asyncio
async def test_create_appointment_invalid_slot():
    payload = {
        "pet_id": VALID_PET_ID,
        "appt_date": "2026-08-20",
        "time_slot": "22:00"  # Horario fuera de rango de trabajo
    }
    async with httpx.AsyncClient() as client:
        response = await client.post(BASE_URL, json=payload)
        
    assert response.status_code == 400


@pytest.mark.asyncio
async def test_create_appointment_pet_not_found():
    payload = {
        "pet_id": INVALID_PET_ID,
        "appt_date": "2026-08-20",
        "time_slot": "10:00"
    }
    async with httpx.AsyncClient() as client:
        response = await client.post(BASE_URL, json=payload)
        
    assert response.status_code == 404



async def make_booking_request(client, payload):
    return await client.post(BASE_URL, json=payload)


@pytest.mark.asyncio
async def test_concurrent_booking_conflict():
    payload = {
        "pet_id": VALID_PET_ID,
        "appt_date": "2026-08-21",
        "time_slot": "15:00"
    }

    async with httpx.AsyncClient() as client:
        task1 = make_booking_request(client, payload)
        task2 = make_booking_request(client, payload)

        response1, response2 = await asyncio.gather(task1, task2)

    status_codes = [response1.status_code, response2.status_code]

    assert 201 in status_codes
    assert 409 in status_codes