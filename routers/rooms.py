from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import Room
from schemas import RoomCreate, RoomOut
from routers.auth import verify_token

router = APIRouter(prefix="/api/rooms", tags=["Rooms"], dependencies=[Depends(verify_token)])


@router.get("", response_model=list[RoomOut])
def get_rooms(db: Session = Depends(get_db)):
    return db.query(Room).all()


@router.post("", response_model=RoomOut, status_code=201)
def create_room(data: RoomCreate, db: Session = Depends(get_db)):
    if db.query(Room).filter(Room.name == data.name).first():
        raise HTTPException(400, f"'{data.name}' xona allaqachon mavjud")
    room = Room(name=data.name, capacity=data.capacity)
    db.add(room)
    db.commit()
    db.refresh(room)
    return room


@router.delete("/{room_id}", status_code=204)
def delete_room(room_id: int, db: Session = Depends(get_db)):
    room = db.get(Room, room_id)
    if not room:
        raise HTTPException(404, "Xona topilmadi")
    db.delete(room)
    db.commit()
