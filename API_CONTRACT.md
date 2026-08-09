# Contrato de API
En este documento se establece la forma de comunicación entre el Frontend y Backend.

# 1. Estándar Global de Errores

Todas las respuestas de error utilizan el código HTTP correspondiente y la siguiente estructura JSON:

{
  "code": "NOMBRE_DEL_ERROR",
  "message": "Mensaje descriptivo para el usuario"
}

# Códigos de Estado HTTP Utilizados:
200 OK: Petición procesada correctamente.
201 Created: Recurso creado exitosamente.
400 Bad Request: Datos de entrada inválidos o faltantes.
409 Conflict: Conflicto de estado (ej. horario reservado por otro usuario).
500 Internal Server Error: Error no esperado en el servidor.

## 2. Horarios

Para simular el contexto real de una peluquería de mascotas, se definen que cada cita tendrá una duración de 1 hora, solo dentro de los tiempos preestablecidos de acuerdo al día de la semana. Suponiendo a su vez que el día domingo no se habre el establecimiento.

Lunes a viernes: Se atiende desde las 9:00 am hasta las 5:00 pm (Hora de almuerzo de 12:00 am a 1:00 pm)

Sábado: Se atiende desde las 9:00 am hasta las 12:00 pm

Domingo: La peluquería se encuentra cerrada.

## 3. Endpoints del Sistema

### Registro (Mascota y Dueño)
Método / Ruta: `POST /api/pets`
Descripción: Registra la información del dueño y la mascota en el sistema.

#### Request Body:
{
  "client_name": "Daniel Rojas",
  "client_email": "daniel@example.com",
  "client_phone": "3291234567",
  "pet_name": "Zeus",
  "pet_species": "Perro"
}

#### Response `201 Created`:
{
  "pet_id": "123e4567-e89b-12d3-a456-426614174000",
  "client_email": "daniel@example.com",
  "pet_name": "Zeus",
  "pet_species": "Perro"
}

#### Response `400 Bad Request`:
{
  "code": "INVALID_INPUT",
  "message": "La especie seleccionada no es válida o faltan campos obligatorios."
}



### Consulta
Método / Ruta: `GET /api/appointments/availability?date=YYYY-MM-DD`
Descripción: Devuelve los bloques de horario del día (09:00 a 17:00) indicando cuáles están disponibles.

#### Query Params:
`date` (string, obligatorio, formato `YYYY-MM-DD`): Fecha a consultar.

#### Response `200 OK`:
{
  "date": "2026-08-10",
  "slots": [
    { "time": "09:00", "available": true },
    { "time": "10:00", "available": false },
    { "time": "11:00", "available": true },
    { "time": "12:00", "available": true },
    { "time": "13:00", "available": true },
    { "time": "14:00", "available": true },
    { "time": "15:00", "available": true },
    { "time": "16:00", "available": true }
  ]
}



### Agendamiento
Método / Ruta: `POST /api/appointments`
Descripción: Crea la reserva de una cita para un bloque de tiempo específico.

#### Request Body:
{
  "pet_id": "123e4567-e89b-12d3-a456-426614174000",
  "appt_date": "2026-08-10",
  "time_slot": "09:00"
}

#### Response `201 Created`:
{
  "appointment_id": "987f6543-e21b-34c5-b678-876543210987",
  "pet_id": "123e4567-e89b-12d3-a456-426614174000",
  "appt_date": "2026-08-10",
  "time_slot": "09:00",
  "status": "confirmada"
}

#### Response `409 Conflict`:
{
  "code": "SLOT_TAKEN",
  "message": "El horario seleccionado fue reservado en el último segundo. Por favor selecciona otro."
}


### Agenda Diaria
Método / Ruta: `GET /api/appointments/daily?date=YYYY-MM-DD`
Descripción: Devuelve el listado de todas las citas agendadas para el día indicado.

#### Query Params:
`date` (string, obligatorio, formato `YYYY-MM-DD`): Fecha a consultar.

#### Response `200 OK`:
{
  "date": "2026-08-10",
  "appointments": [
    {
      "appointment_id": "987f6543-e21b-34c5-b678-876543210987",
      "time_slot": "10:00",
      "pet_name": "Zeus",
      "pet_species": "Perro",
      "client_name": "Daniel Rojas",
      "client_phone": "0991234567"
    }
  ]
}