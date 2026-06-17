from sqlalchemy import Column, Integer, String, ForeignKey, UniqueConstraint, DateTime
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime


class Teacher(Base):
    __tablename__ = "teachers"

    id      = Column(Integer, primary_key=True, index=True)
    name    = Column(String(255), nullable=False)
    phone   = Column(String(30), nullable=True)
    subject_links = relationship("TeacherSubject", back_populates="teacher", cascade="all, delete-orphan")
    class_links   = relationship("TeacherClass",   back_populates="teacher", cascade="all, delete-orphan")
    schedule      = relationship("Schedule",        back_populates="teacher", cascade="all, delete-orphan")


class Subject(Base):
    __tablename__ = "subjects"

    id           = Column(Integer, primary_key=True, index=True)
    name         = Column(String(255), nullable=False, unique=True)
    weekly_hours = Column(Integer, nullable=False, default=3)
    # Generator uchun: fan qiyinligi (1=yengil ... 5=og'ir).
    # Og'ir fanlar tushlikkacha (birinchi soatlarga) joylashtirilishi afzal.
    difficulty   = Column(Integer, nullable=False, default=3)
    # "morning" = faqat tushlikkacha afzal, "any" = istalgan vaqt.
    preferred_time = Column(String(20), nullable=False, default="any")
    teacher_links = relationship("TeacherSubject", back_populates="subject", cascade="all, delete-orphan")
    schedule      = relationship("Schedule",        back_populates="subject", cascade="all, delete-orphan")
    grade_links   = relationship("SubjectGrade",    back_populates="subject", cascade="all, delete-orphan")


class SubjectGrade(Base):
    __tablename__ = "subject_grades"

    subject_id   = Column(Integer, ForeignKey("subjects.id", ondelete="CASCADE"), primary_key=True)
    grade        = Column(Integer, primary_key=True)
    weekly_hours = Column(Integer, nullable=False, default=3)
    subject = relationship("Subject", back_populates="grade_links")


class TeacherSubject(Base):
    __tablename__ = "teacher_subjects"

    teacher_id = Column(Integer, ForeignKey("teachers.id", ondelete="CASCADE"), primary_key=True)
    subject_id = Column(Integer, ForeignKey("subjects.id", ondelete="CASCADE"), primary_key=True)
    teacher = relationship("Teacher", back_populates="subject_links")
    subject = relationship("Subject", back_populates="teacher_links")


class TeacherClass(Base):
    __tablename__ = "teacher_classes"

    teacher_id = Column(Integer, ForeignKey("teachers.id", ondelete="CASCADE"), primary_key=True)
    class_name = Column(String(20), primary_key=True)
    teacher = relationship("Teacher", back_populates="class_links")


class SchoolClass(Base):
    __tablename__ = "classes"

    id               = Column(Integer, primary_key=True, index=True)
    name             = Column(String(20), nullable=False, unique=True)
    grade            = Column(Integer, nullable=False)
    section          = Column(String(5), nullable=False)
    student_count    = Column(Integer, nullable=False, default=30)
    class_teacher_id = Column(Integer, ForeignKey("teachers.id", ondelete="SET NULL"), nullable=True)
    # Smena: 1 = ertalabki, 2 = tushdan keyingi. Generator sinfni faqat
    # o'z smenasiga tegishli soatlarga joylashtiradi.
    shift            = Column(Integer, nullable=False, default=1)


class Room(Base):
    __tablename__ = "rooms"

    id       = Column(Integer, primary_key=True, index=True)
    name     = Column(String(100), nullable=False, unique=True)
    capacity = Column(Integer, nullable=True)


class Schedule(Base):
    __tablename__ = "schedule"

    id         = Column(Integer, primary_key=True, index=True)
    class_id   = Column(String(20), nullable=False)
    teacher_id = Column(Integer, ForeignKey("teachers.id", ondelete="CASCADE"), nullable=False)
    subject_id = Column(Integer, ForeignKey("subjects.id", ondelete="CASCADE"), nullable=False)
    day        = Column(Integer, nullable=False)
    period     = Column(Integer, nullable=False)
    room       = Column(String(100), nullable=True)
    teacher = relationship("Teacher", back_populates="schedule")
    subject = relationship("Subject", back_populates="schedule")

    __table_args__ = (
        UniqueConstraint("class_id",   "day", "period", name="uq_class_time"),
        UniqueConstraint("teacher_id", "day", "period", name="uq_teacher_time"),
    )


class TimeConfig(Base):
    """
    Maktab vaqt sozlamalari (generator uchun global konfiguratsiya).
    Bitta qator (id=1) bo'ladi — butun maktab uchun bitta sozlama.
    """
    __tablename__ = "time_config"

    id              = Column(Integer, primary_key=True, default=1)
    days_count      = Column(Integer, nullable=False, default=6)   # haftada o'quv kunlari (Dush–Shanba)
    # 1-smena soatlari: 1..shift1_periods
    shift1_periods  = Column(Integer, nullable=False, default=6)
    # 2-smena soatlari: shift1_periods+1 .. shift1_periods+shift2_periods
    shift2_periods  = Column(Integer, nullable=False, default=6)
    # Tushlikkacha hisoblanadigan soat chegarasi (shu soatgacha "morning").
    morning_until   = Column(Integer, nullable=False, default=4)


class RefreshToken(Base):
    """Refresh tokenlarni saqlash va boshqarish uchun model"""
    __tablename__ = "refresh_tokens"

    id         = Column(Integer, primary_key=True, index=True)
    jti        = Column(String(255), unique=True, nullable=False, index=True)  # JWT ID
    username   = Column(String(100), nullable=False)
    expires_at = Column(DateTime, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    revoked    = Column(Integer, default=0)  # 0 = active, 1 = revoked
