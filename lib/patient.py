from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from lib.base import Base

class Patient(Base):
    __tablename__ = 'patients'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    age = Column(Integer)
    sex = Column(String)
    drugs = Column(String)
    ward_id = Column(Integer, ForeignKey('wards.id'))
    diagnosis = Column(String)  
    nurse_id = Column(Integer, ForeignKey('nurses.id'))

    # Define relationships
    ward = relationship('Ward', back_populates='patients')
    nurse = relationship('Nurse', back_populates='patients')
     