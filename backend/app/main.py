from fastapi import FastAPI
from app.core.database import Base, engine
from app.routes import health, pets, appointments, clients, admin  
from fastapi.middleware.cors import CORSMiddleware

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="GroomSys API",
    description="API para la gestion de citas de peluqueria canina",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router)
app.include_router(clients.router)
app.include_router(pets.router)
app.include_router(appointments.router)
app.include_router(admin.router) 