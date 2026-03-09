from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from database import Base, engine, get_db
from routers import teachers, subjects, schedule, rooms, auth, classes, report
from routers.auth import verify_token
from schemas import DashboardOut, TeacherLoad
from sqlalchemy.orm import Session
from models import Teacher, Subject, Schedule as ScheduleModel, SchoolClass

# Jadvallarni yaratish (birinchi ishga tushganda)
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="EduPlan API",
    description="Maktab dars jadvali tizimi",
    version="1.0.0",
)

# React (localhost:5173) dan kelgan requestlarga ruxsat
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routerlarni ulash
app.include_router(teachers.router)
app.include_router(subjects.router)
app.include_router(schedule.router)
app.include_router(rooms.router)
app.include_router(auth.router)
app.include_router(classes.router)
app.include_router(report.router)


@app.get("/api/dashboard", response_model=DashboardOut, tags=["Dashboard"], dependencies=[Depends(verify_token)])
def get_dashboard(db: Session = Depends(get_db)):
    all_teachers = db.query(Teacher).all()
    all_schedule = db.query(ScheduleModel).all()

    loads = [
        TeacherLoad(
            id=t.id,
            name=t.name,
            classes=[tc.class_name for tc in t.class_links],
            weekly_lessons=len([e for e in all_schedule if e.teacher_id == t.id]),
        )
        for t in all_teachers
    ]

    return DashboardOut(
        teachers_count=len(all_teachers),
        subjects_count=db.query(Subject).count(),
        lessons_count=len(all_schedule),
        classes_count=db.query(SchoolClass).count(),
        teacher_loads=loads,
    )


@app.get("/", tags=["Root"])
def root():
    return {"status": "ok", "docs": "/docs"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
