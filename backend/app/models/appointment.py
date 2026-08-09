import uuid
from sqlalchemy import Column, String, Date, ForeignKey, DateTime, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base


class AppointmentModel(Base):
    __tablename__ = "appointments"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    pet_id = Column(
        UUID(as_uuid=True), 
        ForeignKey("pets.id", ondelete="CASCADE"), 
        nullable=False
    )
    appt_date = Column(Date, nullable=False)
    time_slot = Column(String(10), nullable=False)
    status = Column(String(20), nullable=False, default="CONFIRMED")
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relacion ORM con PetModel para consultas con JOIN
    pet = relationship("PetModel", back_populates="appointments")

    __table_args__ = (
        UniqueConstraint("appt_date", "time_slot", name="unique_date_time_slot"),
    )