from fastapi import FastAPI
from app.core.database import Base, engine
from app.routes import health

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="GroomSys API",
    description="API para la gestión de citas de peluquería canina",
    version="1.0.0"
)

app.include_router(health.router)