from fastapi import APIRouter, Depends, HTTPException, Query, UploadFile, File
from typing import Optional
from sqlalchemy.orm import Session
import tempfile
import os

from app.db.database import get_db
from app.schemas.carInfo import CarCreate, CarResponse, CarUpdate, AISearchResponse, VoiceSearchResponse
from app.crud.car import create_car, get_all_cars, get_car_by_id, update_car, delete_car, execute_raw_query
from app.core.security import get_current_user
from app.models.user import User
from app.services.llm_service import generate_sql_query
from app.services.voice_service import transcribe_audio

router = APIRouter(
    prefix="/cars",
    tags=["Cars"]
)

@router.post("/", response_model=CarResponse)
def add_car(
    car: CarCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return create_car(db, car)

@router.get("/", response_model=list[CarResponse])
def get_cars(
    db: Session = Depends(get_db),
    name: Optional[str] = Query(None),
    brand: Optional[str] = Query(None),
    model: Optional[str] = Query(None),
    city: Optional[str] = Query(None),
    color: Optional[str] = Query(None),
    fuel_type: Optional[str] = Query(None),
    transmission: Optional[str] = Query(None),
    year: Optional[int] = Query(None),
    min_price: Optional[float] = Query(None),
    max_price: Optional[float] = Query(None),
    min_mileage: Optional[int] = Query(None),
    max_mileage: Optional[int] = Query(None),
):
    return get_all_cars(
        db,
        name=name,
        brand=brand,
        model=model,
        fuel_type=fuel_type,
        transmission=transmission,
        city=city,
        color=color,
        year=year,
        min_price=min_price,
        max_price=max_price,
        min_mileage=min_mileage,
        max_mileage=max_mileage,
    )

@router.get("/ai-search", response_model=AISearchResponse)
def ai_search_cars(
    query: str = Query(..., description="Natural language search e.g. 'red Toyota under 20000'"),
    db: Session = Depends(get_db)
):
    result = generate_sql_query(query)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    sql = result["sql"]
    results = execute_raw_query(db, sql)
    return {"query": sql, "results": results}

@router.post("/voice-search", response_model=VoiceSearchResponse)
def voice_search_cars(
    audio: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(audio.filename)[1]) as tmp:
        tmp.write(audio.file.read())
        tmp_path = tmp.name

    try:
        transcribed_text = transcribe_audio(tmp_path)
        result = generate_sql_query(transcribed_text)
        if "error" in result:
            raise HTTPException(status_code=400, detail=result["error"])
        sql = result["sql"]
        results = execute_raw_query(db, sql)
    finally:
        os.remove(tmp_path)

    return {"transcribed_text": transcribed_text, "query": sql, "results": results}

@router.get("/{car_id}", response_model=CarResponse)
def get_car(car_id: int, db: Session = Depends(get_db)):
    car = get_car_by_id(db, car_id)
    if not car:
        raise HTTPException(status_code=404, detail="Car not found")
    return car

@router.put("/{car_id}", response_model=CarResponse)
def edit_car(
    car_id: int,
    data: CarUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    car = update_car(db, car_id, data)
    if not car:
        raise HTTPException(status_code=404, detail="Car not found")
    return car

@router.delete("/{car_id}")
def remove_car(
    car_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    car = delete_car(db, car_id)
    if not car:
        raise HTTPException(status_code=404, detail="Car not found")
    return {"message": "Car deleted successfully"}
