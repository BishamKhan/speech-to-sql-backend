from sqlalchemy import Column, Integer, String, Float, Text
from app.db.database import Base

class Cars(Base):
    __tablename__ = "cars"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), index=True)
    brand = Column(String(100), index=True)
    model = Column(String(100), index=True)
    city = Column(String(100), index=True)
    color = Column(String(100), index=True)
 
    price = Column(Float, index=True)
    year = Column(Integer, index=True)
    mileage = Column(Integer, index=True)
    fuel_type = Column(String(50), index=True)
    transmission = Column(String(50), index=True)
    condition = Column(String(50), index=True)
    images = Column(String(255), nullable=True)
    description = Column(Text, nullable=True)