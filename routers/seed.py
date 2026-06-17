"""
Seed router — namuna maktab ma'lumotini bazaga yuklash.

Frontenddagi "Bazani yuklash" tugmasi `POST /api/seed` ni chaqiradi.
Ma'lumot manbai: seed_data.py (yagona manba).
"""
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy import text

from database import get_db
from models import (
    Subject, SubjectGrade, SchoolClass, Room, Teacher,
    Schedule, TeacherSubject, TeacherClass,
)
from routers.auth import verify_token
import seed_data as sd

router = APIRouter(prefix="/api/seed", tags=["Seed"], dependencies=[Depends(verify_token)])


class SeedResult(BaseModel):
    ok:        bool
    message:   str
    subjects:  int
    grades:    int   # subject_grades yozuvlari
    classes:   int
    rooms:     int
    teachers:  int


def _wipe(db: Session):
    """
    Mavjud ma'lumotni tozalash (jadval bog'lanishlari tartibida).
    Schedule va biriktirishlar ham o'chadi — toza namuna yuklash uchun.
    Identity (id) larni qayta 1 dan boshlash uchun TRUNCATE ... RESTART IDENTITY.
    """
    db.execute(text(
        "TRUNCATE TABLE schedule, teacher_subjects, teacher_classes, "
        "subject_grades, subjects, classes, rooms, teachers "
        "RESTART IDENTITY CASCADE"
    ))
    db.commit()


@router.post("", response_model=SeedResult)
def load_seed(db: Session = Depends(get_db)):
    """
    Namuna maktab ma'lumotini bazaga yuklash (5–11 sinf).

    **Nima qiladi:**
    - Eski ma'lumotni tozalaydi (schedule, fanlar, sinflar, xonalar, o'qituvchilar)
    - Barcha fanlarni qiyinligi/afzal vaqti bilan qo'shadi
    - Qaysi fan qaysi sinfga, haftasiga necha soat — biriktiradi (subject_grades)
    - Sinflar (5-A ... 11-B), xonalar (oddiy + amaliy laboratoriyalar), o'qituvchilar

    **Eslatma:**
    - Qayta bosilsa — ma'lumot to'liq qayta yuklanadi (idempotent natija)
    - O'qituvchini sinfga biriktirish foydalanuvchi tomonidan keyin qilinadi
    """
    _wipe(db)

    # 1) Fanlar — nom bo'yicha id ni eslab qolamiz
    subj_id = {}
    for name, difficulty, pref, _practical in sd.SUBJECTS:
        s = Subject(name=name, weekly_hours=3, difficulty=difficulty, preferred_time=pref)
        db.add(s)
        db.flush()  # id olish uchun
        subj_id[name] = s.id

    # 2) Sinf-fan-soat (subject_grades)
    grade_count = 0
    for grade, plan in sd.CURRICULUM.items():
        for fan, hours in plan.items():
            db.add(SubjectGrade(subject_id=subj_id[fan], grade=grade, weekly_hours=hours))
            grade_count += 1

    # 3) O'qituvchilar — ismni id ga eslab qolamiz (sinf rahbari uchun kerak)
    teacher_id = {}
    for tname, phone, subj_names in sd.TEACHERS:
        t = Teacher(name=tname, phone=phone)
        db.add(t)
        db.flush()
        teacher_id[tname] = t.id
        # O'qituvchi-fan biriktirish (TeacherSubject)
        for sname in subj_names:
            if sname in subj_id:
                db.add(TeacherSubject(teacher_id=t.id, subject_id=subj_id[sname]))

    # 4) Sinflar — sinf rahbari (class_teacher_id) bilan
    for name, grade, section, students, shift in sd.build_classes():
        ct_name = sd.CLASS_TEACHERS.get(name)
        db.add(SchoolClass(
            name=name, grade=grade, section=section,
            student_count=students, shift=shift,
            class_teacher_id=teacher_id.get(ct_name) if ct_name else None,
        ))

    # 5) Xonalar
    for rname, cap in sd.build_rooms():
        db.add(Room(name=rname, capacity=cap))

    db.commit()

    return SeedResult(
        ok=True,
        message="Namuna maktab ma'lumoti muvaffaqiyatli yuklandi",
        subjects=len(sd.SUBJECTS),
        grades=grade_count,
        classes=len(sd.build_classes()),
        rooms=len(sd.build_rooms()),
        teachers=len(sd.TEACHERS),
    )


@router.delete("")
def clear_seed(db: Session = Depends(get_db)):
    """
    Barcha ma'lumotni tozalash (bazani bo'shatish).

    **Nima qiladi:**
    - Jadval (schedule), o'qituvchi-fan/sinf biriktirishlar, fanlar,
      sinf-fan, sinflar, xonalar, o'qituvchilarni to'liq o'chiradi
    - id larni qayta 1 dan boshlaydi

    **Eslatma:**
    - Bu amal qaytarilmaydi! Foydalanuvchidan tasdiq so'ralishi kerak (frontend).
    """
    _wipe(db)
    return {"ok": True, "message": "Baza tozalandi — barcha ma'lumot o'chirildi"}