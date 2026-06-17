"""
seed_data.py dagi ma'lumotni mustaqil ko'chma `seed.sql` fayliga eksport qiladi.

Foydalanish:
    .venv/bin/python export_seed_sql.py

Natija: seed.sql — uni istalgan PostgreSQL bazaga yuklash mumkin:
    psql -h localhost -U postgres -d maktab_db -f seed.sql

Bu fayl `POST /api/seed` endpoint bilan BIR XIL ma'lumotni beradi
(ikkalasi ham seed_data.py ni manba qiladi).
"""
import seed_data as sd


def esc(s: str) -> str:
    """SQL string uchun bitta tirnoqni ekranlash."""
    return s.replace("'", "''")


def main():
    lines = []
    w = lines.append

    w("-- EduPlan namuna maktab ma'lumoti (5-11 sinf)")
    w("-- seed_data.py dan avtomatik generatsiya qilingan. Qo'lda tahrirlamang.")
    w("-- Yuklash: psql -h localhost -U postgres -d maktab_db -f seed.sql")
    w("")
    w("BEGIN;")
    w("")
    w("-- Eski ma'lumotni tozalash va id larni qayta 1 dan boshlash")
    w("TRUNCATE TABLE schedule, teacher_subjects, teacher_classes,")
    w("    subject_grades, subjects, classes, rooms, teachers")
    w("    RESTART IDENTITY CASCADE;")
    w("")

    # ── Fanlar ───────────────────────────────────────────────
    w("-- Fanlar (id tartibi seed_data.SUBJECTS bilan bir xil)")
    subj_id = {}
    for i, (name, difficulty, pref, _practical) in enumerate(sd.SUBJECTS, start=1):
        subj_id[name] = i
        w(f"INSERT INTO subjects (name, weekly_hours, difficulty, preferred_time) "
          f"VALUES ('{esc(name)}', 3, {difficulty}, '{esc(pref)}');")
    w("")

    # ── Sinf-fan-soat ────────────────────────────────────────
    w("-- Sinf-fan-soat (qaysi fan qaysi sinfga, haftasiga necha soat)")
    for grade in sorted(sd.CURRICULUM):
        for fan, hours in sd.CURRICULUM[grade].items():
            w(f"INSERT INTO subject_grades (subject_id, grade, weekly_hours) "
              f"VALUES ({subj_id[fan]}, {grade}, {hours});")
    w("")

    # ── O'qituvchilar ────────────────────────────────────────
    # Sinflardan OLDIN qo'shamiz, chunki sinflar class_teacher_id orqali murojaat qiladi.
    w("-- O'qituvchilar (id tartibi seed_data.TEACHERS bilan bir xil)")
    teacher_id = {}
    for i, (tname, phone, _subj_names) in enumerate(sd.TEACHERS, start=1):
        teacher_id[tname] = i
        w(f"INSERT INTO teachers (name, phone) VALUES ('{esc(tname)}', '{esc(phone)}');")
    w("")

    # ── O'qituvchi-fan biriktirish ───────────────────────────
    w("-- O'qituvchi-fan biriktirish (qaysi o'qituvchi qaysi fanni o'qitadi)")
    for tname, _phone, subj_names in sd.TEACHERS:
        for sname in subj_names:
            if sname in subj_id:
                w(f"INSERT INTO teacher_subjects (teacher_id, subject_id) "
                  f"VALUES ({teacher_id[tname]}, {subj_id[sname]});")
    w("")

    # ── Sinflar ──────────────────────────────────────────────
    w("-- Sinflar (5-A ... 11-B) — sinf rahbari (class_teacher_id) bilan")
    for name, grade, section, students, shift in sd.build_classes():
        ct_name = sd.CLASS_TEACHERS.get(name)
        ct_id = teacher_id.get(ct_name) if ct_name else None
        ct_val = str(ct_id) if ct_id is not None else "NULL"
        w(f"INSERT INTO classes (name, grade, section, student_count, shift, class_teacher_id) "
          f"VALUES ('{esc(name)}', {grade}, '{esc(section)}', {students}, {shift}, {ct_val});")
    w("")

    # ── Xonalar ──────────────────────────────────────────────
    w("-- Xonalar (oddiy sinf xonalari + amaliy fan laboratoriyalari)")
    for rname, cap in sd.build_rooms():
        w(f"INSERT INTO rooms (name, capacity) VALUES ('{esc(rname)}', {cap});")
    w("")

    w("COMMIT;")
    w("")

    out = "\n".join(lines)
    with open("seed.sql", "w", encoding="utf-8") as f:
        f.write(out)

    # Qisqa hisobot
    total_sg = sum(len(p) for p in sd.CURRICULUM.values())
    total_ts = sum(len(subj_names) for _, _, subj_names in sd.TEACHERS)
    print("seed.sql yaratildi:")
    print(f"  fanlar:           {len(sd.SUBJECTS)}")
    print(f"  sinf-fan:         {total_sg}")
    print(f"  o'qituvchilar:    {len(sd.TEACHERS)}")
    print(f"  o'qituvchi-fan:   {total_ts}")
    print(f"  sinf rahbarlari:  {len(sd.CLASS_TEACHERS)}")
    print(f"  sinflar:          {len(sd.build_classes())}")
    print(f"  xonalar:          {len(sd.build_rooms())}")


if __name__ == "__main__":
    main()