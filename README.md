# GroomSys - Sistema de Gestión de Citas para Peluquería Canina

## Descripción del Producto

GroomSys es una plataforma web desarrollada como un Producto Mínimo Viable (MVP) para la gestión integral de citas, clientes y mascotas en peluquerías caninas. 

El sistema resuelve la problemática de agendamientos duplicados por concurrencia (*race conditions*) y optimiza el flujo de atención mediante la verificación inteligente de usuarios existentes y la administración centralizada de horarios. Ofrece una interfaz intuitiva para los dueños de mascotas y un panel administrativo completo para la visualización del negocio.

---

## Arquitectura Propuesta

El proyecto está estructurado en un monorepositorio con dos componentes totalmente independientes para cumplir con las buenas prácticas de desarrollo y desacoplamiento:

* **Backend (`/backend`):** Desarrollado en Python con FastAPI y PostgreSQL/Supabase. Encargado de la lógica de negocio, validación de datos con Pydantic, gestión de concurrencia mediante transacciones SQL y exposición de la API RESTful.
* **Frontend (`/frontend`):** Desarrollado en React. Interfaz gráfica encargada del flujo del usuario (verificación de email, registro de mascota, selección de horarios y vista de administrador).

### Módulos Principales de la API:
* **`clients`:** Verificación rápida de registro por email y creación de clientes.
* **`pets`:** Registro e identificación inteligente de mascotas vinculadas a dueños existentes.
* **`appointments`:** Consulta de disponibilidad de franjas horarias y agendamiento seguro contra reservas concurrentes.
* **`admin`:** Autenticación de administradores y generación de reportes semanales de citas.

---

## Tecnologías y Herramientas Utilizadas

### Backend
* **FastAPI:** Framework web moderno y de alto rendimiento para Python, utilizado por su velocidad y generación automática de documentación Swagger OpenAPI.
* **SQLAlchemy & PostgreSQL / Supabase:** ORM para la manipulación de la base de datos relacional alojada en la nube de Supabase.
* **Pydantic:** Garantiza la validación estricta de datos de entrada/salida y manejo estructurado de errores.
* **Pytest & HTTPX:** Suite de pruebas unitarias e integración para validar la lógica de negocio, autenticación y concurrencia.
* **Uvicorn:** Servidor ASGI para la ejecución local y en producción del servicio web.

### Frontend
* **React:** Librería base para la construcción de interfaces modulares y dinámicas.
* **Vite:** Herramienta de compilación y servidor de desarrollo rápido.
* **Tailwind CSS:** Framework de estilos utilitarios para el diseño responsivo.

---

## Supuestos Realizados

* **Horarios de Atención y Duración:** Se asume que cada servicio de peluquería tiene una duración exacta de 1 hora. La atención es de lunes a viernes (09:00 a 17:00, con receso de 12:00 a 13:00) y sábados (09:00 a 12:00).
* **Especies Admitidas:** El sistema está acotado en esta fase inicial exclusivamente a las especies `"Perro"` y `"Gato"`.
* **Manejo de Concurrencia:** Se asume un entorno de alta demanda, por lo que las reservas de turnos están protegidas en la base de datos para responder con código `409 Conflict` si dos usuarios intentan tomar la misma franja en el mismo segundo.
* **Sesiones Administrador:** La autenticación administrativa valida credenciales de acceso directo para acceder a la agenda semanal de citas.

---

## Mejoras Futuras (Con más tiempo)

* **Recordatorios Automáticos por WhatsApp/Email:** Notificar a los clientes 24 horas antes de la cita programada.
* **Historial Médico y Notas de Grooming:** Permitir guardar observaciones específicas sobre el corte o salud de la mascota en citas pasadas.
* **Gestión de Empleados/Peluqueros:** Asignar peluqueros específicos a cada franja disponible para multiplicar los cupos concurrentes.
* **Cancelación y Reagendamiento en Línea:** Permitir al cliente cancelar o cambiar la fecha de su reserva mediante un token enviado a su correo.

---

## Pasos para Correr el Proyecto Localmente

1. Ingresar a la carpeta backend, dentro de ella se activa el entorno a travez del comando ".venv\Scripts\activate".

2. Instalar las dependenciar "pip install -r requirements.txt".

3. Iniciar el servidor con el comando "python -m uvicorn app.main:app --reload".

4. A través de otra terminal activar el servidor de frontend, redirigiendose a la carpeta para luego correr el comando "npm run dev".

5. Dirigirse a la dirección que se imprime en la terminal.
