from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from models import Schedule, Subject, TeacherSubject, SchoolClass
from schemas import ReportOut, SubjectStatOut, DayStatOut
from routers.auth import verify_token

router = APIRouter(prefix="/api/report", tags=["Report"], dependencies=[Depends(verify_token)])

DAYS_UZ = ["Dushanba", "Seshanba", "Chorshanba", "Payshanba", "Juma", "Shanba"]


@router.get("", response_model=ReportOut)
def get_report(db: Session = Depends(get_db)):
    all_schedule = db.query(Schedule).all()
    all_subjects = db.query(Subject).order_by(Subject.name).all()
    all_classes  = db.query(SchoolClass).all()

    filled = len(all_schedule)
    total  = len(all_classes) * 6 * 7  # 6 kun, 7 dars

    day_stats = [
        DayStatOut(day=DAYS_UZ[i], count=sum(1 for e in all_schedule if e.day == i))
        for i in range(6)
    ]

    subject_stats = []
    for s in all_subjects:
        count         = sum(1 for e in all_schedule if e.subject_id == s.id)
        teacher_count = db.query(TeacherSubject).filter(TeacherSubject.subject_id == s.id).count()
        subject_stats.append(SubjectStatOut(id=s.id, name=s.name, count=count, teachers=teacher_count))
    subject_stats.sort(key=lambda x: x.count, reverse=True)

    return ReportOut(
        total_slots=total,
        filled_slots=filled,
        fill_percent=round(filled / total * 100) if total > 0 else 0,
        total_students=sum(c.student_count for c in all_classes),
        day_stats=day_stats,
        subject_stats=subject_stats,
    )
