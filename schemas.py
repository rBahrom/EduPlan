from pydantic import BaseModel
from typing import Optional


# ─── TEACHER ─────────────────────────────────────────────────────────────────

class TeacherCreate(BaseModel):
    name:  str
    phone: Optional[str] = None


class TeacherAssign(BaseModel):
    """Fan va sinf biriktirish (AssignSubjectModal)"""
    subject_ids: list[int]
    class_names: list[str]


class TeacherOut(BaseModel):
    id:       int
    name:     str
    phone:    Optional[str]
    subjects: list[int]    # subject id lar
    classes:  list[str]    # sinf nomlari

    class Config:
        from_attributes = True


# ─── SUBJECT ─────────────────────────────────────────────────────────────────

class SubjectCreate(BaseModel):
    name:         str
    weekly_hours: int = 3


class SubjectOut(BaseModel):
    id:           int
    name:         str
    weekly_hours: int

    class Config:
        from_attributes = True


class SubjectGradeCreate(BaseModel):
    subject_id:   int
    grade:        int
    weekly_hours: int = 3


class SubjectGradeOut(BaseModel):
    subject_id:   int
    grade:        int
    weekly_hours: int
    name:         str  # subjects.name dan join

    class Config:
        from_attributes = True


# ─── SCHEDULE ────────────────────────────────────────────────────────────────

class ScheduleCreate(BaseModel):
    class_id:   str         # "5-A"
    teacher_id: int
    subject_id: int
    day:        int         # 0–5
    period:     int         # 1–6
    room:       Optional[str] = None


class ScheduleOut(BaseModel):
    id:         int
    class_id:   str
    teacher_id: int
    subject_id: int
    day:        int
    period:     int
    room:       Optional[str]

    class Config:
        from_attributes = True


# ─── CLASS ───────────────────────────────────────────────────────────────────

class ClassCreate(BaseModel):
    name:             str
    grade:            int
    section:          str
    student_count:    int = 30
    class_teacher_id: Optional[int] = None


class ClassOut(BaseModel):
    id:               int
    name:             str
    grade:            int
    section:          str
    student_count:    int
    class_teacher_id: Optional[int]

    class Config:
        from_attributes = True


# ─── ROOM ────────────────────────────────────────────────────────────────────

class RoomCreate(BaseModel):
    name:     str
    capacity: Optional[int] = None


class RoomOut(BaseModel):
    id:       int
    name:     str
    capacity: Optional[int]

    class Config:
        from_attributes = True


# ─── CONFLICTS ───────────────────────────────────────────────────────────────

class ConflictOut(BaseModel):
    type: str   # "class" | "teacher" | "room"
    msg:  str


# ─── SWAP ─────────────────────────────────────────────────────────────────────

class SwapTeacherOut(BaseModel):
    id:   int
    name: str


class SwapLessonOut(BaseModel):
    lesson_id:    int
    class_id:     str
    period:       int
    subject_id:   int
    subject_name: str
    possible:     list[SwapTeacherOut]


class DoSwapRequest(BaseModel):
    lesson_id:      int
    new_teacher_id: int


# ─── REPORT ───────────────────────────────────────────────────────────────────

class SubjectStatOut(BaseModel):
    id:       int
    name:     str
    count:    int
    teachers: int


class DayStatOut(BaseModel):
    day:   str
    count: int


class ReportOut(BaseModel):
    total_slots:    int
    filled_slots:   int
    fill_percent:   int
    total_students: int
    day_stats:      list[DayStatOut]
    subject_stats:  list[SubjectStatOut]


# ─── AUTH ─────────────────────────────────────────────────────────────────────

class LoginIn(BaseModel):
    username: str
    password: str


class LoginOut(BaseModel):
    access: bool
    token:  str


# ─── DASHBOARD ───────────────────────────────────────────────────────────────

class TeacherLoad(BaseModel):
    id:         int
    name:       str
    classes:    list[str]
    weekly_lessons: int


class DashboardOut(BaseModel):
    teachers_count: int
    subjects_count: int
    lessons_count:  int
    classes_count:  int
    teacher_loads:  list[TeacherLoad]
