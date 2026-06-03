from sqlalchemy.orm import Session
from sqlalchemy import text
from fastapi import HTTPException
from app.models.carInfo import Cars
from app.schemas.carInfo import CarCreate, CarUpdate

def create_car(db: Session, car: CarCreate):
    new_car = Cars(**car.model_dump())
    db.add(new_car)
    db.commit()
    db.refresh(new_car)
    return new_car

def get_all_cars(
    db: Session,
    name: str = None,
    brand: str = None,
    model: str = None,
    city: str = None,
    color: str = None,
    fuel_type: str = None,
    transmission: str = None,
    year: int = None,
    min_price: float = None,
    max_price: float = None,
    min_mileage: int = None,
    max_mileage: int = None,
):
    query = db.query(Cars)

    if name:
        query = query.filter(Cars.name.ilike(f"%{name}%"))
    if brand:
        query = query.filter(Cars.brand.ilike(f"%{brand}%"))
    if model:
        query = query.filter(Cars.model.ilike(f"%{model}%"))
    if city:
        query = query.filter(Cars.city.ilike(f"%{city}%"))
    if color:
        query = query.filter(Cars.color.ilike(f"%{color}%"))
    if fuel_type:
        query = query.filter(Cars.fuel_type.ilike(f"%{fuel_type}%"))
    if transmission:
        query = query.filter(Cars.transmission.ilike(f"%{transmission}%"))
    if year:
        query = query.filter(Cars.year == year)
    if min_price is not None:
        query = query.filter(Cars.price >= min_price)
    if max_price is not None:
        query = query.filter(Cars.price <= max_price)
    if min_mileage is not None:
        query = query.filter(Cars.mileage >= min_mileage)
    if max_mileage is not None:
        query = query.filter(Cars.mileage <= max_mileage)

    return query.all()

def get_car_by_id(db: Session, car_id: int):
    return db.query(Cars).filter(Cars.id == car_id).first()

def update_car(db: Session, car_id: int, data: CarUpdate):
    car = db.query(Cars).filter(Cars.id == car_id).first()
    if not car:
        return None
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(car, field, value)
    db.commit()
    db.refresh(car)
    return car

def execute_raw_query(db: Session, sql: str):
    sql_upper = sql.strip().upper()
    if not sql_upper.startswith("SELECT"):
        raise HTTPException(status_code=400, detail="Only SELECT queries are allowed")
    for keyword in ["INSERT", "UPDATE", "DELETE", "DROP", "ALTER", "TRUNCATE"]:
        if keyword in sql_upper:
            raise HTTPException(status_code=400, detail="Only SELECT queries are allowed")
    result = db.execute(text(sql))
    return result.mappings().all()

def delete_car(db: Session, car_id: int):
    car = db.query(Cars).filter(Cars.id == car_id).first()
    if car:
        db.delete(car)
        db.commit()
    return car
