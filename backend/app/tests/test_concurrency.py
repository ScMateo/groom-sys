import asyncio
import httpx
import pytest

# URL base de tu API local
BASE_URL = "http://127.0.0.1:8000/api/appointments"

# Reemplaza este UUID por un pet_id valido que exista en tu base de datos
VALID_PET_ID = "41c513e9-dac5-4350-a862-49980ca2a773"  


async def make_booking_request(client, payload):
    """Realiza una peticion POST asincrona para reservar cita."""
    return await client.post(BASE_URL, json=payload)


@pytest.mark.asyncio
async def test_concurrent_booking_conflict():
    """
    Simula dos peticiones concurrentes enviadas en paralelo exacto
    al mismo slot y fecha para verificar la proteccion contra doble reserva.
    """
    payload = {
        "pet_id": VALID_PET_ID,
        "appt_date": "2026-08-15",
        "time_slot": "12:00"
    }

    async with httpx.AsyncClient() as client:
        # Disparar ambas peticiones en paralelo real usando asyncio.gather
        task1 = make_booking_request(client, payload)
        task2 = make_booking_request(client, payload)

        response1, response2 = await asyncio.gather(task1, task2)

    status_codes = [response1.status_code, response2.status_code]

    # Verificar que exactamente una haya sido exitosa (201) y la otra rechazada (409)
    assert 201 in status_codes, "Una de las peticiones debio responder 201 Created"
    assert 409 in status_codes, "La peticion concurrente debio responder 409 Conflict"