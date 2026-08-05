from fastapi import FastAPI
from app.core.database import Base, engine
from app.routes import health, pets, appointments

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="GroomSys API",
    description="API para la gestión de citas de peluquería canina",
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
app.include_router(pets.router)
app.include_router(appointments.router)