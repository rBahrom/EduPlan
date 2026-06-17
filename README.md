# EduPlan - Maktab Dars Jadvali Tizimi

Maktablar uchun avtomatlashtirilgan dars jadvali boshqaruv tizimi.

## 🎯 Loyiha Haqida

EduPlan - bu maktablarda dars jadvallarini tuzish, boshqarish va nazorat qilish uchun mo'ljallangan zamonaviy web ilovasi.

## ✨ Asosiy Funksiyalar

- O'qituvchilar, fanlar, sinflar va xonalarni boshqarish
- Avtomatik konflikt tekshiruvi bilan jadval yaratish
- O'qituvchi almashtirish tizimi
- Hisobot va statistika
- JWT token autentifikatsiyasi

## 🚀 Ishga Tushirish

### Ikkalasini birdan (tavsiya etiladi)
```bash
.venv/bin/python run.py
# Backend :8070 + Frontend :5173 bir vaqtda. To'xtatish: Ctrl+C
```

### Backend
```bash
.venv/bin/python -m uvicorn main:app --reload --port 8070
# http://localhost:8070
```

### Frontend
```bash
cd frond && npm run dev
# http://localhost:5173
```

### API Dokumentatsiya
- http://localhost:8070/docs

## 🗄️ Namuna ma'lumot (seed)

5–11 sinf fanlari, sinflar, xonalar va o'qituvchilarni bazaga yuklash uchun
ikki yo'l bor:

1. **Tugma orqali** — ilovaga kirib, Dashboard'dagi **"Namuna bazani yuklash"**
   tugmasini bosing (`POST /api/seed`).
2. **SQL fayl orqali** — ko'chma `seed.sql` ni to'g'ridan-to'g'ri yuklang:
   ```bash
   psql -h localhost -U postgres -d maktab_db -f seed.sql
   ```
   `seed.sql` ni qayta generatsiya qilish: `.venv/bin/python export_seed_sql.py`

> Eslatma: seed yuklash mavjud ma'lumotni (jadval, fanlar, sinflar, xonalar,
> o'qituvchilar) tozalab, qaytadan to'ldiradi.

## 📖 To'liq Dokumentatsiya

- [API.md](./API.md) - API qo'llanmasi
- [http://localhost:8000/docs](http://localhost:8000/docs) - Swagger UI

---

**© 2026 EduPlan**
