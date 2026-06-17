from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import SchoolClass
from schemas import ClassCreate, ClassOut
from routers.auth import verify_token

router = APIRouter(prefix="/api/classes", tags=["Classes"], dependencies=[Depends(verify_token)])


@router.get("", response_model=list[ClassOut])
def get_classes(db: Session = Depends(get_db)):
    """
    Barcha sinflar ro'yxatini olish

    **Qaytaradi:**
    - Sinflar ro'yxati (sinf va bo'lim bo'yicha tartiblangan)

    **Misol:**
    - 5-A, 5-B, 6-A, 6-B, ...
    """
    return db.query(SchoolClass).order_by(SchoolClass.grade, SchoolClass.section).all()


@router.post("", response_model=ClassOut, status_code=201)
def create_class(data: ClassCreate, db: Session = Depends(get_db)):
    """
    Yangi sinf qo'shish

    **Parametrlar:**
    - **name**: Sinf nomi (masalan: "5-A", "10-B")
    - **grade**: Sinf darajasi (1-11)
    - **section**: Bo'lim (A, B, V, G...)
    - **student_count**: O'quvchilar soni (default: 30)
    - **class_teacher_id**: Sinf rahbari ID (ixtiyoriy)

    **Qaytaradi:**
    - Yaratilgan sinf ma'lumotlari

    **Xatolik:**
    - 400: Sinf allaqachon mavjud bo'lsa
    """
    if db.query(SchoolClass).filter(SchoolClass.name == data.name).first():
        raise HTTPException(400, f"'{data.name}' sinfi allaqachon mavjud")
    cls = SchoolClass(
        name=data.name,
        grade=data.grade,
        section=data.section,
        student_count=data.student_count,
        class_teacher_id=data.class_teacher_id,
        shift=data.shift,
    )
    db.add(cls)
    db.commit()
    db.refresh(cls)
    return cls


@router.delete("/{class_id}", status_code=204)
def delete_class(class_id: int, db: Session = Depends(get_db)):
    """
    Sinfni o'chirish

    **Parametrlar:**
    - **class_id**: Sinf ID raqami

    **Xatolik:**
    - 404: Sinf topilmasa
    """
    cls = db.get(SchoolClass, class_id)
    if not cls:
        raise HTTPException(404, "Sinf topilmadi")
    db.delete(cls)
    db.commit()