from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import Subject, SubjectGrade
from schemas import SubjectCreate, SubjectOut, SubjectGradeCreate, SubjectGradeOut
from routers.auth import verify_token

router = APIRouter(prefix="/api/subjects", tags=["Subjects"], dependencies=[Depends(verify_token)])


@router.get("", response_model=list[SubjectOut])
def get_subjects(db: Session = Depends(get_db)):
    return db.query(Subject).order_by(Subject.name).all()


@router.post("", response_model=SubjectOut, status_code=201)
def create_subject(data: SubjectCreate, db: Session = Depends(get_db)):
    if db.query(Subject).filter(Subject.name == data.name).first():
        raise HTTPException(400, f"'{data.name}' fani allaqachon mavjud")
    subject = Subject(name=data.name, weekly_hours=data.weekly_hours)
    db.add(subject)
    db.commit()
    db.refresh(subject)
    return subject


@router.delete("/{subject_id}", status_code=204)
def delete_subject(subject_id: int, db: Session = Depends(get_db)):
    subject = db.get(Subject, subject_id)
    if not subject:
        raise HTTPException(404, "Fan topilmadi")
    db.delete(subject)
    db.commit()


# ── Subject-Grade (sinf-fan bog'liq) ──────────────────────────────────────────

@router.get("/grades", response_model=list[SubjectGradeOut])
def get_subject_grades(db: Session = Depends(get_db)):
    rows = db.query(SubjectGrade, Subject.name).join(Subject).order_by(SubjectGrade.grade, Subject.name).all()
    return [
        SubjectGradeOut(subject_id=sg.subject_id, grade=sg.grade, weekly_hours=sg.weekly_hours, name=name)
        for sg, name in rows
    ]


@router.post("/grades", response_model=SubjectGradeOut, status_code=201)
def add_subject_to_grade(data: SubjectGradeCreate, db: Session = Depends(get_db)):
    subject = db.get(Subject, data.subject_id)
    if not subject:
        raise HTTPException(404, "Fan topilmadi")
    if db.get(SubjectGrade, (data.subject_id, data.grade)):
        raise HTTPException(400, f"'{subject.name}' fani {data.grade}-sinfga allaqachon biriktirilgan")
    sg = SubjectGrade(subject_id=data.subject_id, grade=data.grade, weekly_hours=data.weekly_hours)
    db.add(sg)
    db.commit()
    return SubjectGradeOut(subject_id=sg.subject_id, grade=sg.grade, weekly_hours=sg.weekly_hours, name=subject.name)


@router.delete("/grades/{subject_id}/{grade}", status_code=204)
def remove_subject_from_grade(subject_id: int, grade: int, db: Session = Depends(get_db)):
    sg = db.get(SubjectGrade, (subject_id, grade))
    if not sg:
        raise HTTPException(404, "Bog'liq topilmadi")
    db.delete(sg)
    db.commit()
