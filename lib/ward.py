from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base

class Ward(Base):
    __tablename__ = 'wards'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    doctor_id = Column(Integer, ForeignKey('doctors.id'))

    doctor = relationship("Doctor", back_populates="wards")
    nurses = relationship("Nurse", back_populates="ward")
    patients = relationship("Patient", back_populates="ward")
