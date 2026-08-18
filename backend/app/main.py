from fastapi import FastAPI
from app.core.database import Base, engine
from app.routes import health, pets, appointments, clients, admin  
from fastapi.middleware.cors import CORSMiddleware

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="GroomSys API",
    description="API para la gestion de citas de peluqueria canina",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configuración de CORS habilitada para desarrollo y producción
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite conexiones desde cualquier origen (Frontend en Vercel/Netlify o Local)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Endpoint raíz para verificar el estado de la API en producción
@app.get("/")
def read_root():
    return {
        "status": "online",
        "message": "Bienvenido a la API de GroomSys",
        "documentation": "/docs"
    }

# Registrar los routers del sistema
app.include_router(health.router)
app.include_router(clients.router)
app.include_router(pets.router)
app.include_router(appointments.router)
app.include_router(admin.router)