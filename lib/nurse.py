from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base

class Nurse(Base):
    __tablename__ = 'nurses'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    age = Column(Integer, nullable=False)
    ward_id = Column(Integer, ForeignKey('wards.id'), nullable=False)

    ward = relationship("Ward", back_populates="nurses")
    patients = relationship("Patient", back_populates="nurse") 
