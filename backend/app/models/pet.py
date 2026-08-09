import uuid
from sqlalchemy import Column, String, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base


class PetModel(Base):
    __tablename__ = "pets"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    client_id = Column(
        UUID(as_uuid=True), 
        ForeignKey("clients.id", ondelete="CASCADE"), 
        nullable=False
    )
    name = Column(String(50), nullable=False)
    species = Column(String(30), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relacion con ClientModel
    client = relationship("ClientModel", back_populates="pets")

    # Relacion inversa con AppointmentModel necesaria para SQLAlchemy
    appointments = relationship("AppointmentModel", back_populates="pet", cascade="all, delete-orphan")

    __table_args__ = (
        UniqueConstraint("client_id", "name", name="uq_client_pet_name"),
    )