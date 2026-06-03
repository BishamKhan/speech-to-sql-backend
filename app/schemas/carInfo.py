from pydantic import BaseModel
from typing import Optional

class CarCreate(BaseModel):
    name: str
    brand: str
    model: str
    price: float
    year: int
    city: str
    color: str
    mileage: int
    fuel_type: str
    transmission: str
    condition: str
    images: Optional[str] = None
    description: Optional[str] = None

class CarUpdate(BaseModel):
    name: Optional[str] = None
    brand: Optional[str] = None
    model: Optional[str] = None
    price: Optional[float] = None
    year: Optional[int] = None
    city: Optional[str] = None
    color: Optional[str] = None
    mileage: Optional[int] = None
    fuel_type: Optional[str] = None
    transmission: Optional[str] = None
    condition: Optional[str] = None
    images: Optional[str] = None
    description: Optional[str] = None

class CarResponse(CarCreate):
    id: int

    class Config:
        from_attributes = True

class AISearchResponse(BaseModel):
    query: str
    results: list[CarResponse]

class VoiceSearchResponse(BaseModel):
    transcribed_text: str
    query: str
    results: list[CarResponse]
