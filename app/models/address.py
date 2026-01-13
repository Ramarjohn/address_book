from sqlalchemy import Column, Float, Integer, String
from app.db.base import Base

class Address(Base):
    __tablename__ = "addresses"

    id = Column(Integer, primary_key=True, index=True)
    label = Column(String(120), nullable=True)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    postal_code = Column(String(20), nullable=True, unique=True, index=True)
    country = Column(String(100), nullable=True)
    state = Column(String(100), nullable=True)
    city = Column(String(100), nullable=True)
    district = Column(String(100), nullable=True)
    street = Column(String(200), nullable=True)
