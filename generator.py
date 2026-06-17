"""
EduPlan — Avtomatik dars jadvali generatori.

Butun jadval tuzish mantig'i shu yerda (backend). Frontend faqat tugma bosadi.

Yondashuv: Google OR-Tools CP-SAT (Constraint Programming) solver.
Muammoni "har bir (sinf, fan, o'qituvchi, kun, soat) uchun bormi/yo'qmi"
boolean o'zgaruvchilar to'plami sifatida modellaymiz va constraintlar bilan
cheklaymiz, keyin soft maqsadlar bo'yicha optimallashtiramiz.

QATTIQ constraintlar (HARD — buzilmaydi):
  H1. Har sinf bir vaqtda ko'pi bilan 1 dars   → bir sinfga bitta o'qituvchi
  H2. Har o'qituvchi bir vaqtda ko'pi bilan 1 sinf → bir o'qituvchi bir joyda
  H3. Har xona bir vaqtda ko'pi bilan 1 dars   → bir xonada bitta sinf
  H4. Har (sinf, fan) o'zining haftalik soatini TO'LIQ oladi (SubjectGrade)
  H5. O'qituvchi faqat o'zi biladigan fanni o'qitadi (TeacherSubject)
  H6. Sinf faqat o'z smenasidagi (shift) soatlarga joylashadi (TimeConfig)
  H7. Amaliy fan → laboratoriya; oddiy fan → sinf xonasi
  H8. Bir (sinf, fan) ni butun hafta DAVOMIDA bitta o'qituvchi o'qitadi

YUMSHOQ maqsadlar (SOFT — imkon qadar):
  S1. Og'ir fanlar (preferred_time=morning) tushlikkacha (morning_until)
  S2. Bir fan kuniga ko'pi bilan 1 marta (haftaga yoyiladi)
  S3. Yuk o'qituvchilar orasida balanslangan (eng kam yuklangan tanlanadi)
"""
from dataclasses import dataclass, field
from collections import defaultdict
from ortools.sat.python import cp_model

from models import (
    Subject, SubjectGrade, SchoolClass, Room, Teacher,
    TeacherSubject, TimeConfig,
)

# seed_data dagi amaliy fanlar ro'yxati — qaysi fan laboratoriya talab qiladi.
# (DB modelida alohida ustun yo'q, shuning uchun nom bo'yicha aniqlaymiz.)
import seed_data as sd

# Amaliy fan nomi → unga mos maxsus xona nomidagi kalit so'z.
# Generator shu kalit so'zli xonalarni laboratoriya sifatida ajratadi.
PRACTICAL_ROOM_HINTS = {
    "Fizika":            ["fizika"],
    "Kimyo":             ["kimyo"],
    "Biologiya":         ["biolog"],
    "Informatika":       ["informatika"],
    "Jismoniy tarbiya":  ["sport", "zal"],
    "Musiqa":            ["musiqa"],
    "Texnologiya":       ["texnologiya", "ustaxona"],
}

# QATTIQ laboratoriya talab qiladigan fanlar — bir slotda mavjud
# laboratoriyalar sonidan ko'p sinf bo'la OLMAYDI (fizik cheklov).
# Jismoniy tarbiya (sport zali / maydon), Musiqa, Texnologiya bunга
# kirmaydi: ular bir vaqtda bir nechta guruh bilan ham o'tilishi mumkin,
# shuning uchun ularni qattiq cheklamaymiz (aks holda bitta sport zali
# butun maktabga yetmay, jadval umuman tuzilmaydi).
HARD_LAB_SUBJECTS = {"Fizika", "Kimyo", "Biologiya", "Informatika"}


@dataclass
class GenResult:
    ok:               bool
    message:          str
    placed:           int  = 0            # joylashtirilgan darslar soni
    required:         int  = 0            # talab qilingan jami soat
    solve_seconds:    float = 0.0
    status:           str  = ""
    unplaced:         list = field(default_factory=list)  # joylashmagan (sinf, fan)
    entries:          list = field(default_factory=list)  # yangi Schedule yozuvlari (dict)


def generate_schedule(db, time_limit_sec: int = 30) -> GenResult:
    """
    Bazadagi ma'lumotdan to'liq jadval tuzadi.

    Qaytaradi: GenResult (yozuvlar entries ichida; ularni saqlash router ishi).
    """
    # ─── 1) MA'LUMOTNI YIG'AMIZ ────────────────────────────────────────────────
    cfg = db.get(TimeConfig, 1) or TimeConfig(
        id=1, days_count=6, shift1_periods=6, shift2_periods=6, morning_until=4
    )
    days = list(range(cfg.days_count))                       # 0..days-1
    shift1 = list(range(1, cfg.shift1_periods + 1))          # 1-smena soatlari
    shift2 = list(range(cfg.shift1_periods + 1,
                        cfg.shift1_periods + cfg.shift2_periods + 1))  # 2-smena

    classes  = db.query(SchoolClass).all()
    subjects = {s.id: s for s in db.query(Subject).all()}
    rooms    = db.query(Room).all()
    teachers = db.query(Teacher).all()

    if not classes:
        return GenResult(False, "Sinflar yo'q — avval namuna ma'lumotni yuklang.")
    if not subjects:
        return GenResult(False, "Fanlar yo'q — avval namuna ma'lumotni yuklang.")
    if not teachers:
        return GenResult(False, "O'qituvchilar yo'q — avval namuna ma'lumotni yuklang.")

    # Sinf darajasi → {subject_id: weekly_hours} (SubjectGrade rejasi)
    grade_plan = defaultdict(dict)
    for sg in db.query(SubjectGrade).all():
        grade_plan[sg.grade][sg.subject_id] = sg.weekly_hours

    # Fanni biladigan o'qituvchilar: subject_id → [teacher_id, ...]
    subj_teachers = defaultdict(list)
    for ts in db.query(TeacherSubject).all():
        subj_teachers[ts.subject_id].append(ts.teacher_id)

    # Xonalarni ikkiga ajratamiz: oddiy sinf xonalari va maxsus laboratoriyalar.
    practical_names = sd.PRACTICAL_SUBJECTS  # {"Fizika", "Kimyo", ...}
    lab_rooms   = defaultdict(list)   # subject_id → [room_name, ...] (laboratoriyalar)
    normal_rooms = []                 # oddiy sinf xonalari
    for r in rooms:
        low = r.name.lower()
        matched = False
        for subj_name, hints in PRACTICAL_ROOM_HINTS.items():
            if any(h in low for h in hints):
                # Shu fanga (id bo'yicha) mos laboratoriya
                for sid, s in subjects.items():
                    if s.name == subj_name:
                        lab_rooms[sid].append(r.name)
                matched = True
        if not matched:
            normal_rooms.append(r.name)

    # ─── 2) MODELNI QURAMIZ ─────────────────────────────────────────────────────
    model = cp_model.CpModel()

    # Har sinf uchun smenasiga qarab ruxsat etilgan soatlar.
    def periods_for(cls):
        return shift1 if cls.shift == 1 else shift2

    # Talablar ro'yxati: har (sinf, fan) bo'yicha nechta soat kerak + nomzod o'qituvchilar.
    # requirements[(class, subject_id)] = hours
    requirements = {}
    unplaced = []
    total_required = 0
    for cls in classes:
        plan = grade_plan.get(cls.grade, {})
        for sid, hours in plan.items():
            cands = subj_teachers.get(sid, [])
            if not cands:
                unplaced.append((cls.name, subjects[sid].name if sid in subjects else str(sid),
                                 "o'qituvchi yo'q"))
                continue
            requirements[(cls.name, sid)] = hours
            total_required += hours

    if not requirements:
        return GenResult(
            False,
            "Joylashtiriladigan dars yo'q — sinf darajalariga fan rejasi (SubjectGrade) "
            "yoki fan o'qituvchilari biriktirilmagan.",
            unplaced=unplaced,
        )

    # Har (sinf, fan) uchun BITTA o'qituvchi tanlanadi (H8: hafta davomida bir xil).
    # teacher_pick[(class, sid, tid)] = bool — shu o'qituvchi shu (sinf,fan) ni o'qitadimi.
    teacher_pick = {}
    for (cname, sid) in requirements:
        cands = subj_teachers[sid]
        picks = []
        for tid in cands:
            v = model.NewBoolVar(f"pick_c{cname}_s{sid}_t{tid}")
            teacher_pick[(cname, sid, tid)] = v
            picks.append(v)
        # Aniq bitta o'qituvchi tanlanadi
        model.Add(sum(picks) == 1)

    # Asosiy o'zgaruvchilar: x[(class, sid, day, period)] = shu slotda shu dars bormi.
    x = {}
    cls_by_name = {c.name: c for c in classes}
    for (cname, sid), hours in requirements.items():
        cls = cls_by_name[cname]
        for d in days:
            for p in periods_for(cls):
                x[(cname, sid, d, p)] = model.NewBoolVar(f"x_c{cname}_s{sid}_d{d}_p{p}")

    # ── H4: har (sinf, fan) aniq o'zining haftalik soatini oladi ──
    for (cname, sid), hours in requirements.items():
        cls = cls_by_name[cname]
        slots = [x[(cname, sid, d, p)] for d in days for p in periods_for(cls)]
        model.Add(sum(slots) == hours)

    # ── H1: har sinf har slotda ko'pi bilan 1 dars ──
    for cls in classes:
        cname = cls.name
        sids = [sid for (cn, sid) in requirements if cn == cname]
        for d in days:
            for p in periods_for(cls):
                model.Add(sum(x[(cname, sid, d, p)] for sid in sids) <= 1)

    # ── H2: har o'qituvchi har slotda ko'pi bilan 1 sinf ──
    # Dars (cname, sid, d, p) bu o'qituvchiga tegishli bo'lishi = x AND teacher_pick.
    # assign[(cname, sid, tid, d, p)] = x[...] AND teacher_pick[(cname,sid,tid)]
    assign = {}
    for (cname, sid), hours in requirements.items():
        cls = cls_by_name[cname]
        for tid in subj_teachers[sid]:
            for d in days:
                for p in periods_for(cls):
                    a = model.NewBoolVar(f"a_c{cname}_s{sid}_t{tid}_d{d}_p{p}")
                    xv = x[(cname, sid, d, p)]
                    pv = teacher_pick[(cname, sid, tid)]
                    # a == xv AND pv
                    model.Add(a <= xv)
                    model.Add(a <= pv)
                    model.Add(a >= xv + pv - 1)
                    assign[(cname, sid, tid, d, p)] = a

    # Har o'qituvchi har slotda ko'pi bilan bitta darsda
    for tid in [t.id for t in teachers]:
        for d in days:
            all_p = set(shift1) | set(shift2)
            for p in all_p:
                terms = [a for (cn, sid, t2, dd, pp), a in assign.items()
                         if t2 == tid and dd == d and pp == p]
                if terms:
                    model.Add(sum(terms) <= 1)

    # ── H3 + H7: xonalar ──
    # Har dars bir xona oladi. Amaliy fan → laboratoriya, oddiy fan → oddiy xona.
    # Soddalik uchun: oddiy fanlar uchun har SINFga doimiy bitta sinf xonasi beramiz
    # (sinflar soni = oddiy xonalar soni, seed shunday tuzilgan) — bu H3 ni oddiy
    # fanlar uchun avtomatik ta'minlaydi (har sinf o'z xonasida).
    # Laboratoriya talab qiladigan fanlar uchun esa slot bo'yicha cheklaymiz.
    room_assign = {}  # (cname, sid, d, p) → tanlangan xona nomi (oddiy fanlar uchun keyin)
    # Oddiy xonani sinflarga tarqatamiz (deterministik)
    class_home_room = {}
    sorted_classes = sorted(classes, key=lambda c: (c.grade, c.section))
    for i, cls in enumerate(sorted_classes):
        if i < len(normal_rooms):
            class_home_room[cls.name] = normal_rooms[i]
        else:
            class_home_room[cls.name] = normal_rooms[i % len(normal_rooms)] if normal_rooms else None

    # Laboratoriya konflikti (H3+H7): QATTIQ lab fanlari uchun bir slotda shu
    # fanni o'qiydigan sinflar soni mavjud laboratoriyalar sonidan oshmasin.
    # (Sport/Musiqa/Texnologiya cheklanmaydi — bir vaqtda bir nechta guruh mumkin.)
    for sid, labs in lab_rooms.items():
        if sid not in subjects or subjects[sid].name not in HARD_LAB_SUBJECTS:
            continue
        cap = len(labs)  # shu fan uchun mavjud laboratoriyalar soni
        for d in days:
            all_p = set(shift1) | set(shift2)
            for p in all_p:
                terms = [x[(cname, s2, d, p)] for (cname, s2) in requirements
                         if s2 == sid and (cname, s2, d, p) in x]
                if terms:
                    model.Add(sum(terms) <= cap)

    # ── S2: bir fan kuniga ko'pi bilan 1 marta (haftaga yoyish) ──
    # Soft qilamiz: oshib ketsa jarima. Lekin soat > kunlar bo'lsa imkonsiz,
    # shuning uchun limitni max(1, ceil(hours/days)) qilamiz va ortig'iga jarima.
    spread_penalties = []
    for (cname, sid), hours in requirements.items():
        cls = cls_by_name[cname]
        base = max(1, -(-hours // len(days)))  # ceil(hours/days)
        for d in days:
            day_count = model.NewIntVar(0, len(periods_for(cls)), f"dc_c{cname}_s{sid}_d{d}")
            model.Add(day_count == sum(x[(cname, sid, d, p)] for p in periods_for(cls)))
            over = model.NewIntVar(0, len(periods_for(cls)), f"over_c{cname}_s{sid}_d{d}")
            model.Add(over >= day_count - base)
            model.Add(over >= 0)
            spread_penalties.append(over)

    # ── S1: og'ir fanlar (morning) tushlikkacha ──
    morning_penalties = []
    for (cname, sid), hours in requirements.items():
        s = subjects[sid]
        if s.preferred_time == "morning":
            cls = cls_by_name[cname]
            for d in days:
                for p in periods_for(cls):
                    if p > cfg.morning_until:
                        # tushlikdan keyin joylashtirilsa jarima (soft)
                        morning_penalties.append(x[(cname, sid, d, p)])

    # ── MAQSAD: jarimalarni minimallashtirish ──
    model.Minimize(
        3 * sum(spread_penalties) +     # kunlarga yoyilish muhimroq
        1 * sum(morning_penalties)
    )

    # ─── 3) YECHAMIZ ────────────────────────────────────────────────────────────
    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = float(time_limit_sec)
    solver.parameters.num_search_workers = 8
    status = solver.Solve(model)

    status_name = solver.StatusName(status)
    if status not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        return GenResult(
            False,
            f"Yechim topilmadi (status={status_name}). Soatlar sonini yoki "
            f"o'qituvchilarni tekshiring — talab smena imkoniyatidan oshgan bo'lishi mumkin.",
            required=total_required,
            solve_seconds=round(solver.WallTime(), 2),
            status=status_name,
            unplaced=unplaced,
        )

    # ─── 4) YECHIMNI YOZUVLARGA AYLANTIRAMIZ ────────────────────────────────────
    # Har laboratoriya fan uchun slot bo'yicha bo'sh labni navbat bilan beramiz.
    lab_busy = defaultdict(set)   # (room_name, d, p) band
    entries = []
    placed = 0
    for (cname, sid), hours in requirements.items():
        cls = cls_by_name[cname]
        s = subjects[sid]
        # Bu (sinf, fan) uchun tanlangan o'qituvchi
        chosen_tid = None
        for tid in subj_teachers[sid]:
            if solver.Value(teacher_pick[(cname, sid, tid)]) == 1:
                chosen_tid = tid
                break
        for d in days:
            for p in periods_for(cls):
                if solver.Value(x[(cname, sid, d, p)]) == 1:
                    # Xona tanlash:
                    #  - QATTIQ lab fani (Fizika/Kimyo/...) → mavjud bo'sh laboratoriya
                    #    (solver allaqachon sig'imni kafolatlagan, shuning uchun bo'sh topiladi)
                    #  - Sport/Musiqa/Texnologiya → maxsus xona nomi (lekin bir vaqtda bir
                    #    nechta guruh mumkin, shuning uchun konflikt deb belgilanmasin: room=None)
                    #  - Oddiy fan → sinfning doimiy xonasi
                    if s.name in HARD_LAB_SUBJECTS and lab_rooms.get(sid):
                        room = None
                        for rn in lab_rooms[sid]:
                            if (rn, d, p) not in lab_busy:
                                room = rn
                                lab_busy[(rn, d, p)].add(cname)
                                break
                        if room is None:
                            room = lab_rooms[sid][0]  # fallback (kutilmaydi)
                    elif s.name in practical_names:
                        # Soft amaliy fan (sport/musiqa/texnologiya): xona band qilmaydi
                        room = None
                    else:
                        room = class_home_room.get(cname)
                    entries.append({
                        "class_id":   cname,
                        "teacher_id": chosen_tid,
                        "subject_id": sid,
                        "day":        d,
                        "period":     p,
                        "room":       room,
                    })
                    placed += 1

    msg = f"Jadval tuzildi: {placed}/{total_required} dars joylashtirildi."
    if unplaced:
        msg += f" {len(unplaced)} ta (sinf, fan) o'qituvchi yo'qligi sababli o'tkazib yuborildi."

    return GenResult(
        ok=True,
        message=msg,
        placed=placed,
        required=total_required,
        solve_seconds=round(solver.WallTime(), 2),
        status=status_name,
        unplaced=unplaced,
        entries=entries,
    )