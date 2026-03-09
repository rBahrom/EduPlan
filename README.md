# EduPlan — Maktab Dars Jadvali Tizimi

> Maktablarda o'qituvchilar va sinflar uchun to'qnashuvlarsiz dars jadvali tuzish tizimi.
> Hozirda tizim test rejimida kundalik.com bilan integratsiya amalga oshmoqda
---

## Loyiha haqida

**EduPlan** — o'zbek maktablari uchun ishlab chiqilgan zamonaviy dars jadvali boshqaruv tizimi. Tizim bir o'qituvchi bir vaqtda ikki sinfda dars o'tishini, yoki bir sinfga bir vaqtda ikki dars belgilanishini **avtomatik ravishda oldini oladi**.

### Asosiy muammolar va yechimlar

| Muammo | EduPlan yechimi |
|--------|-----------------|
| O'qituvchi bir vaqtda 2 sinfga belgilanadi | DB darajasida unique constraint + backend validatsiya |
| Bir sinfga bir vaqtda 2 ta dars tushadi | Jadval tuzishda ziddiyat tekshiruvi |
| Qo'lda jadval tuzish ko'p vaqt oladi | Qulay UI orqali tez jadval yaratish |
| O'qituvchilarni almashtirish murakkab | Swap mexanizmi — mavjud darslarni almashtirish |

---

## Texnologiyalar

### Backend
- **FastAPI** — yuqori tezlikdagi Python API framework
- **SQLAlchemy 2.0** — ORM va ma'lumotlar bazasi boshqaruvi
- **PostgreSQL** — asosiy ma'lumotlar bazasi
- **Pydantic v2** — ma'lumot validatsiyasi va schemalar
- **Uvicorn** — ASGI server

### Frontend
- **React** (Vite) — komponent asosidagi UI
- **CSS** — moslashtirilgan dizayn

---

## Imkoniyatlar

### O'qituvchilar boshqaruvi
- O'qituvchi qo'shish, tahrirlash, o'chirish
- Har bir o'qituvchiga fanlar va sinflar biriktirish
- O'qituvchi yuklamasi (haftaiga necha dars) statistikasi

### Fanlar va sinflar
- Fan qo'shish va sinf darajasiga bog'lash
- Har bir fan uchun haftalik soatni sozlash (sinf bo'yicha)
- 5–11 sinflar, A/B/C bo'limlar

### Dars jadvali
- 6 kunlik jadval (Dushanba–Shanba)
- Har kuni 7 ta dars davri (08:00–15:15)
- Xona biriktirish imkoniyati
- Filtr: sinf yoki o'qituvchi bo'yicha ko'rish

### Ziddiyat (Conflict) boshqaruvi
- Real-time ziddiyat aniqlab berish
- Sinf, o'qituvchi va xona ziddiyatlarini alohida ko'rsatish
- O'qituvchilarni almashtirish (Swap) — fan mutaxassisligini hisobga olgan holda

### Hisobot va statistika
- Jadval to'ldirilganlik foizi
- Kunlik va fan bo'yicha tahlil
- O'qituvchi yuklamasi umumiy ko'rinishi

---

## Arxitektura

```
maktab_fast/
├── backend/
│   ├── main.py              # FastAPI ilovasi, CORS, routerlar
│   ├── database.py          # SQLAlchemy ulanishi
│   ├── models.py            # Ma'lumotlar bazasi modellari
│   ├── schemas.py           # Pydantic schemalar
│   ├── requirements.txt     # Python kutubxonalari
│   └── routers/
│       ├── auth.py          # Autentifikatsiya
│       ├── teachers.py      # O'qituvchilar CRUD
│       ├── subjects.py      # Fanlar va sinf darajalari
│       ├── classes.py       # Sinflar CRUD
│       ├── rooms.py         # Xonalar CRUD
│       ├── schedule.py      # Jadval, ziddiyat, swap
│       └── report.py        # Hisobot va statistika
└── frond/
    └── src/
        ├── main.jsx         # React kirish nuqtasi
        └── eduplan_v2.jsx   # Asosiy UI ilovasi
```

---

## Ma'lumotlar bazasi modeli

```
Teacher ────────── TeacherSubject ── Subject
   │                                    │
   └────────── TeacherClass          SubjectGrade
                                        │
SchoolClass ── Schedule ──────── (grade)
   │               │
Room ──────────────┘
```

**Schedule jadvalidagi cheklovlar:**
- `UNIQUE(class_id, day, period)` — bir sinfga bir vaqtda bitta dars
- `UNIQUE(teacher_id, day, period)` — bir o'qituvchi bir vaqtda bitta joyda

---

## O'rnatish va ishga tushirish

### Talablar
- Python 3.10+
- PostgreSQL 14+
- Node.js 18+ (frontend uchun)

### Backend

```bash
cd backend

# Virtual muhit yaratish
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Kutubxonalarni o'rnatish
pip install -r requirements.txt

# .env fayl yaratish
cp .env.example .env
# DATABASE_URL ni sozlang

# Serverni ishga tushirish
uvicorn main:app --reload --port 8000
```

### Frontend

```bash
cd frond

npm install
npm run dev
```

### .env namuna

```env
DATABASE_URL=postgresql://postgres:password@localhost:5432/maktab_db
ADMIN_USERNAME=admin
ADMIN_PASSWORD=admin123
SECRET_TOKEN=eduplan-secret-2024
```

---

## API Endpointlar

| Method | URL | Tavsif |
|--------|-----|--------|
| `POST` | `/api/auth/login` | Tizimga kirish |
| `GET` | `/api/teachers` | O'qituvchilar ro'yxati |
| `POST` | `/api/teachers` | O'qituvchi qo'shish |
| `PUT` | `/api/teachers/{id}/assign` | Fan/sinf biriktirish |
| `GET` | `/api/subjects` | Fanlar ro'yxati |
| `POST` | `/api/subjects/grades` | Fanni sinf darajasiga bog'lash |
| `GET` | `/api/classes` | Sinflar ro'yxati |
| `GET` | `/api/rooms` | Xonalar ro'yxati |
| `GET` | `/api/schedule` | Dars jadvali |
| `POST` | `/api/schedule` | Dars qo'shish |
| `GET` | `/api/schedule/conflicts` | Ziddiyatlarni ko'rish |
| `POST` | `/api/schedule/swap` | O'qituvchilarni almashtirish |
| `GET` | `/api/report` | Hisobot |
| `GET` | `/api/dashboard` | Dashboard statistika |

API dokumentatsiyasi: [http://localhost:8000/docs](http://localhost:8000/docs)

---

## Xavfsizlik eslatmalari (Production)

- `CORS allow_origins=["*"]` — ishlab chiqarishda domenni cheklang
- `SECRET_TOKEN` — murakkab va noyob token ishlatilsin
- JWT autentifikatsiyasiga o'tish tavsiya etiladi
- `dashboard` endpointidagi `SessionLocal()` ni `get_db()` dependency ga almashtiring

---

## Litsenziya

MIT License — bu loyihani erkin ishlatishingiz, o'zgartirishingiz va tarqatishingiz mumkin.
