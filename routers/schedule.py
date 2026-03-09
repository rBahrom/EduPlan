from collections import defaultdict
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional
from database import get_db
from models import Schedule, Teacher, Subject, TeacherSubject
from schemas import ScheduleCreate, ScheduleOut, ConflictOut, SwapLessonOut, SwapTeacherOut, DoSwapRequest
from routers.auth import verify_token

router = APIRouter(prefix="/api/schedule", tags=["Schedule"], dependencies=[Depends(verify_token)])

VALID_DAYS    = range(0, 6)   # 0=Dushanba, 5=Shanba
VALID_PERIODS = range(1, 8)   # 1–7
DAYS_UZ = ["Dushanba","Seshanba","Chorshanba","Payshanba","Juma","Shanba"]


def _check_conflict(db: Session, data: ScheduleCreate, exclude_id: Optional[int] = None) -> str | None:
    """
    Sinf yoki o'qituvchi bir vaqtda ikki joyda bo'lmasligi uchun tekshiruv.
    Frontenda (eduplan.jsx:126) ham bor, lekin backend zarur chunki:
    - Bir vaqtda ikki request kelsa race condition bo'ladi
    - DB UNIQUE constraint xato kodi chiqaradi, bu esa foydalanuvchiga noaniq
    """
    q = db.query(Schedule).filter(
        Schedule.day == data.day,
        Schedule.period == data.period,
    )
    if exclude_id:
        q = q.filter(Schedule.id != exclude_id)

    # Sinf bandi?
    if q.filter(Schedule.class_id == data.class_id).first():
        return f"❌ Sinf konflikti: {data.class_id} bu vaqtda allaqachon band!"

    # O'qituvchi bandi?
    if q.filter(Schedule.teacher_id == data.teacher_id).first():
        teacher = db.get(Teacher, data.teacher_id)
        return f"❌ O'qituvchi konflikti: {teacher.name} bu vaqtda boshqa sinfda!"

    return None


@router.get("", response_model=list[ScheduleOut])
def get_schedule(
    class_id:   Optional[str] = Query(None, description="Sinf bo'yicha filter: 5-A"),
    teacher_id: Optional[int] = Query(None, description="O'qituvchi bo'yicha filter"),
    db: Session = Depends(get_db),
):
    q = db.query(Schedule)
    if class_id:
        q = q.filter(Schedule.class_id == class_id)
    if teacher_id:
        q = q.filter(Schedule.teacher_id == teacher_id)
    return q.all()


@router.post("", response_model=ScheduleOut, status_code=201)
def create_entry(data: ScheduleCreate, db: Session = Depends(get_db)):
    # Qiymat oralig'ini tekshirish
    if data.day not in VALID_DAYS:
        raise HTTPException(400, "day 0–5 orasida bo'lishi kerak")
    if data.period not in VALID_PERIODS:
        raise HTTPException(400, "period 1–6 orasida bo'lishi kerak")

    # Konflikt tekshiruvi
    conflict = _check_conflict(db, data)
    if conflict:
        raise HTTPException(409, conflict)

    entry = Schedule(**data.model_dump())
    db.add(entry)
    db.commit()
    db.refresh(entry)
    return entry


@router.delete("/{entry_id}", status_code=204)
def delete_entry(entry_id: int, db: Session = Depends(get_db)):
    entry = db.get(Schedule, entry_id)
    if not entry:
        raise HTTPException(404, "Dars topilmadi")
    db.delete(entry)
    db.commit()


# ── Konfliktlar ───────────────────────────────────────────────────────────────

@router.get("/conflicts", response_model=list[ConflictOut])
def get_conflicts(db: Session = Depends(get_db)):
    all_entries = db.query(Schedule).all()
    slots = defaultdict(list)
    for e in all_entries:
        slots[(e.day, e.period)].append(e)

    conflicts = []
    seen = set()
    for (day, period), entries in slots.items():
        day_name = DAYS_UZ[day]
        for i in range(len(entries)):
            for j in range(i + 1, len(entries)):
                a, b = entries[i], entries[j]
                pair = tuple(sorted([a.id, b.id]))

                if a.class_id == b.class_id:
                    key = ("class", *pair)
                    if key not in seen:
                        seen.add(key)
                        sa = db.get(Subject, a.subject_id)
                        sb = db.get(Subject, b.subject_id)
                        conflicts.append(ConflictOut(
                            type="class",
                            msg=f"{a.class_id} sinfi {day_name} {period}-darsda 2 ta dars: {sa.name if sa else '?'} va {sb.name if sb else '?'}"
                        ))

                if a.teacher_id == b.teacher_id:
                    key = ("teacher", *pair)
                    if key not in seen:
                        seen.add(key)
                        t = db.get(Teacher, a.teacher_id)
                        conflicts.append(ConflictOut(
                            type="teacher",
                            msg=f"{t.name if t else '?'} — {day_name} {period}-darsda {a.class_id} va {b.class_id} da bir vaqtda"
                        ))

                if a.room and b.room and a.room == b.room:
                    key = ("room", *pair)
                    if key not in seen:
                        seen.add(key)
                        conflicts.append(ConflictOut(
                            type="room",
                            msg=f"{a.room} — {day_name} {period}-darsda {a.class_id} va {b.class_id} band"
                        ))

    return conflicts


# ── Almashtirish ──────────────────────────────────────────────────────────────

@router.get("/swap", response_model=list[SwapLessonOut])
def find_swap(
    teacher_id: int = Query(...),
    day: int        = Query(...),
    db: Session     = Depends(get_db),
):
    lessons = db.query(Schedule).filter(
        Schedule.teacher_id == teacher_id,
        Schedule.day == day,
    ).all()
    if not lessons:
        raise HTTPException(404, "Bu kunda darsi yo'q")

    # Bu kunda band bo'lgan o'qituvchilar (period bo'yicha)
    busy_by_period = defaultdict(set)
    for s in db.query(Schedule).filter(Schedule.day == day).all():
        busy_by_period[s.period].add(s.teacher_id)

    results = []
    for lesson in lessons:
        subj = db.get(Subject, lesson.subject_id)
        candidate_ids = [
            ts.teacher_id for ts in
            db.query(TeacherSubject).filter(
                TeacherSubject.subject_id == lesson.subject_id,
                TeacherSubject.teacher_id != teacher_id,
            ).all()
        ]
        possible = []
        for tid in candidate_ids:
            if tid not in busy_by_period[lesson.period]:
                t = db.get(Teacher, tid)
                if t:
                    possible.append(SwapTeacherOut(id=t.id, name=t.name))

        results.append(SwapLessonOut(
            lesson_id=lesson.id,
            class_id=lesson.class_id,
            period=lesson.period,
            subject_id=lesson.subject_id,
            subject_name=subj.name if subj else "",
            possible=possible,
        ))
    return results


@router.post("/swap", response_model=ScheduleOut)
def do_swap(data: DoSwapRequest, db: Session = Depends(get_db)):
    lesson = db.get(Schedule, data.lesson_id)
    if not lesson:
        raise HTTPException(404, "Dars topilmadi")

    conflict = db.query(Schedule).filter(
        Schedule.teacher_id == data.new_teacher_id,
        Schedule.day == lesson.day,
        Schedule.period == lesson.period,
        Schedule.id != lesson.id,
    ).first()
    if conflict:
        raise HTTPException(409, "Yangi o'qituvchi bu vaqtda band")

    lesson.teacher_id = data.new_teacher_id
    db.commit()
    db.refresh(lesson)
    return lesson
