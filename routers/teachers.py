from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import Teacher, TeacherSubject, TeacherClass, Subject
from schemas import TeacherCreate, TeacherAssign, TeacherOut
from routers.auth import verify_token

router = APIRouter(prefix="/api/teachers", tags=["Teachers"], dependencies=[Depends(verify_token)])


def _build_out(teacher: Teacher) -> TeacherOut:
    return TeacherOut(
        id=teacher.id,
        name=teacher.name,
        phone=teacher.phone,
        subjects=[ts.subject_id for ts in teacher.subject_links],
        classes=[tc.class_name for tc in teacher.class_links],
    )


@router.get("", response_model=list[TeacherOut])
def get_teachers(db: Session = Depends(get_db)):
    teachers = db.query(Teacher).all()
    return [_build_out(t) for t in teachers]


@router.post("", response_model=TeacherOut, status_code=201)
def create_teacher(data: TeacherCreate, db: Session = Depends(get_db)):
    teacher = Teacher(name=data.name, phone=data.phone)
    db.add(teacher)
    db.commit()
    db.refresh(teacher)
    return _build_out(teacher)


@router.delete("/{teacher_id}", status_code=204)
def delete_teacher(teacher_id: int, db: Session = Depends(get_db)):
    teacher = db.get(Teacher, teacher_id)
    if not teacher:
        raise HTTPException(404, "O'qituvchi topilmadi")
    db.delete(teacher)
    db.commit()


@router.put("/{teacher_id}/assign", response_model=TeacherOut)
def assign_subjects_classes(teacher_id: int, data: TeacherAssign, db: Session = Depends(get_db)):
    teacher = db.get(Teacher, teacher_id)
    if not teacher:
        raise HTTPException(404, "O'qituvchi topilmadi")

    # Fanlar mavjudligini tekshirish
    for sid in data.subject_ids:
        if not db.get(Subject, sid):
            raise HTTPException(404, f"Fan {sid} topilmadi")

    # Eski yozuvlarni o'chirib yangilarini yozish
    db.query(TeacherSubject).filter(TeacherSubject.teacher_id == teacher_id).delete()
    db.query(TeacherClass).filter(TeacherClass.teacher_id == teacher_id).delete()

    for sid in data.subject_ids:
        db.add(TeacherSubject(teacher_id=teacher_id, subject_id=sid))
    for cls in data.class_names:
        db.add(TeacherClass(teacher_id=teacher_id, class_name=cls))

    db.commit()
    db.refresh(teacher)
    return _build_out(teacher)
