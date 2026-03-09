from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import ClassSubject, SchoolClass, Subject
from schemas import ClassSubjectCreate, ClassSubjectOut
from routers.auth import verify_token

router = APIRouter(prefix="/api/classes", tags=["Class-Subjects"], dependencies=[Depends(verify_token)])


@router.get("/{class_id}/subjects", response_model=list[ClassSubjectOut])
def get_class_subjects(class_id: int, db: Session = Depends(get_db)):
    if not db.get(SchoolClass, class_id):
        raise HTTPException(404, "Sinf topilmadi")
    links = db.query(ClassSubject).filter(ClassSubject.class_id == class_id).all()
    return [
        ClassSubjectOut(
            subject_id=l.subject_id,
            weekly_hours=l.weekly_hours,
            subject_name=l.subject.name,
        )
        for l in links
    ]


@router.post("/{class_id}/subjects", response_model=ClassSubjectOut, status_code=201)
def assign_subject(class_id: int, data: ClassSubjectCreate, db: Session = Depends(get_db)):
    if not db.get(SchoolClass, class_id):
        raise HTTPException(404, "Sinf topilmadi")
    subject = db.get(Subject, data.subject_id)
    if not subject:
        raise HTTPException(404, "Fan topilmadi")
    existing = db.query(ClassSubject).filter(
        ClassSubject.class_id == class_id,
        ClassSubject.subject_id == data.subject_id,
    ).first()
    if existing:
        raise HTTPException(400, f"'{subject.name}' bu sinfga allaqachon biriktirilgan")
    link = ClassSubject(class_id=class_id, subject_id=data.subject_id, weekly_hours=data.weekly_hours)
    db.add(link)
    db.commit()
    db.refresh(link)
    return ClassSubjectOut(subject_id=link.subject_id, weekly_hours=link.weekly_hours, subject_name=subject.name)


@router.delete("/{class_id}/subjects/{subject_id}", status_code=204)
def remove_subject(class_id: int, subject_id: int, db: Session = Depends(get_db)):
    link = db.query(ClassSubject).filter(
        ClassSubject.class_id == class_id,
        ClassSubject.subject_id == subject_id,
    ).first()
    if not link:
        raise HTTPException(404, "Birikma topilmadi")
    db.delete(link)
    db.commit()
