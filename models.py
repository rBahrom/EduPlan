from sqlalchemy import Column, Integer, String, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from database import Base


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
