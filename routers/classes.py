from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import SchoolClass
from schemas import ClassCreate, ClassOut
from routers.auth import verify_token

router = APIRouter(prefix="/api/classes", tags=["Classes"], dependencies=[Depends(verify_token)])


@router.get("", response_model=list[ClassOut])
def get_classes(db: Session = Depends(get_db)):
    return db.query(SchoolClass).order_by(SchoolClass.grade, SchoolClass.section).all()


@router.post("", response_model=ClassOut, status_code=201)
def create_class(data: ClassCreate, db: Session = Depends(get_db)):
    if db.query(SchoolClass).filter(SchoolClass.name == data.name).first():
        raise HTTPException(400, f"'{data.name}' sinfi allaqachon mavjud")
    cls = SchoolClass(
        name=data.name,
        grade=data.grade,
        section=data.section,
        student_count=data.student_count,
        class_teacher_id=data.class_teacher_id,
    )
    db.add(cls)
    db.commit()
    db.refresh(cls)
    return cls


@router.delete("/{class_id}", status_code=204)
def delete_class(class_id: int, db: Session = Depends(get_db)):
    cls = db.get(SchoolClass, class_id)
    if not cls:
        raise HTTPException(404, "Sinf topilmadi")
    db.delete(cls)
    db.commit()
