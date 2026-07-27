import uuid
from sqlalchemy import Column, String, DateTime, UniqueConstraint, Index
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from app.core.database import Base

class PetModel(Base):
    __tablename__ = "pets"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    client_name = Column(String(100), nullable=False)
    client_email = Column(String(255), nullable=False, index=True)
    client_phone = Column(String(20), nullable=False)
    pet_name = Column(String(50), nullable=False)
    pet_species = Column(String(30), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Restricción e Índice único crítico: Previene duplicar la misma mascota para un mismo email
    __table_args__ = (
        UniqueConstraint('client_email', 'pet_name', name='uq_client_email_pet_name'),
        Index('idx_client_email_pet_name', 'client_email', 'pet_name'),
    )