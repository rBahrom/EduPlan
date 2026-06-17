# EduPlan API Qo'llanmasi

Maktab dars jadvali tizimi uchun to'liq API dokumentatsiyasi.

**Base URL:** `http://localhost:8000`
**API Docs:** `http://localhost:8000/docs`

---

## 📋 Mundarija

1. [Autentifikatsiya](#1-autentifikatsiya-auth)
2. [O'qituvchilar](#2-oqituvchilar-teachers)
3. [Fanlar](#3-fanlar-subjects)
4. [Sinflar](#4-sinflar-classes)
5. [Xonalar](#5-xonalar-rooms)
6. [Dars Jadvali](#6-dars-jadvali-schedule)
7. [Hisobot](#7-hisobot-report)
8. [Dashboard](#8-dashboard)

---

## 1. Autentifikatsiya (Auth)

Base: `/api/auth`

### 1.1 Login - Tizimga kirish

**Endpoint:** `POST /api/auth/login`

**Vazifa:** Foydalanuvchi login va parol bilan tizimga kiradi, access va refresh tokenlarni oladi.

**Request Body:**
```json
{
  "username": "admin",
  "password": "admin123"
}
```

**Response (200 OK):**
```json
{
  "access": true,
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

**Token muddatlari:**
- Access token: 30 daqiqa
- Refresh token: 7 kun

**Xatoliklar:**
- `401 Unauthorized` - Login yoki parol noto'g'ri

---

### 1.2 Refresh - Yangi access token olish

**Endpoint:** `POST /api/auth/refresh`

**Vazifa:** Refresh token bilan yangi access token olish (access token muddati tugaganda).

**Request Body:**
```json
{
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

**Response (200 OK):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

**Xatoliklar:**
- `401 Unauthorized` - Refresh token noto'g'ri, bekor qilingan yoki muddati tugagan

---

### 1.3 Logout - Tizimdan chiqish

**Endpoint:** `POST /api/auth/logout`

**Vazifa:** Refresh tokenni bekor qilish va tizimdan chiqish.

**Headers:**
```
Authorization: Bearer <access_token>
```

**Request Body:**
```json
{
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

**Response (200 OK):**
```json
{
  "message": "Muvaffaqiyatli chiqildi"
}
```

---

## 2. O'qituvchilar (Teachers)

Base: `/api/teachers`
**🔒 Himoyalangan:** Barcha endpointlar access token talab qiladi

### 2.1 Barcha o'qituvchilarni olish

**Endpoint:** `GET /api/teachers`

**Vazifa:** Barcha o'qituvchilar ro'yxatini olish (fanlar va sinflar bilan).

**Response (200 OK):**
```json
[
  {
    "id": 1,
    "name": "Ahmadov Ali",
    "phone": "+998901234567",
    "subjects": [1, 3],
    "classes": ["5-A", "5-B", "6-A"]
  }
]
```

---

### 2.2 Yangi o'qituvchi qo'shish

**Endpoint:** `POST /api/teachers`

**Vazifa:** Yangi o'qituvchi qo'shish.

**Request Body:**
```json
{
  "name": "Karimova Malika",
  "phone": "+998901234567"
}
```

**Response (201 Created):**
```json
{
  "id": 2,
  "name": "Karimova Malika",
  "phone": "+998901234567",
  "subjects": [],
  "classes": []
}
```

---

### 2.3 O'qituvchini o'chirish

**Endpoint:** `DELETE /api/teachers/{teacher_id}`

**Vazifa:** O'qituvchini va unga bog'liq barcha ma'lumotlarni o'chirish.

**Response:** `204 No Content`

**Xatoliklar:**
- `404 Not Found` - O'qituvchi topilmadi

---

### 2.4 O'qituvchiga fanlar va sinflarni biriktirish

**Endpoint:** `PUT /api/teachers/{teacher_id}/assign`

**Vazifa:** O'qituvchiga qaysi fanlarni qaysi sinflarda o'qitishini belgilash.

**Request Body:**
```json
{
  "subject_ids": [1, 3, 5],
  "class_names": ["5-A", "5-B", "6-A"]
}
```

**Response (200 OK):**
```json
{
  "id": 1,
  "name": "Ahmadov Ali",
  "phone": "+998901234567",
  "subjects": [1, 3, 5],
  "classes": ["5-A", "5-B", "6-A"]
}
```

**Xatoliklar:**
- `404 Not Found` - O'qituvchi yoki fan topilmadi

---

## 3. Fanlar (Subjects)

Base: `/api/subjects`
**🔒 Himoyalangan:** Barcha endpointlar access token talab qiladi

### 3.1 Barcha fanlarni olish

**Endpoint:** `GET /api/subjects`

**Vazifa:** Barcha fanlar ro'yxatini olish (alifbo tartibida).

**Response (200 OK):**
```json
[
  {
    "id": 1,
    "name": "Matematika",
    "weekly_hours": 5
  },
  {
    "id": 2,
    "name": "Fizika",
    "weekly_hours": 3
  }
]
```

---

### 3.2 Yangi fan qo'shish

**Endpoint:** `POST /api/subjects`

**Vazifa:** Yangi fan qo'shish.

**Request Body:**
```json
{
  "name": "Kimyo",
  "weekly_hours": 3
}
```

**Response (201 Created):**
```json
{
  "id": 3,
  "name": "Kimyo",
  "weekly_hours": 3
}
```

**Xatoliklar:**
- `400 Bad Request` - Fan allaqachon mavjud

---

### 3.3 Fanni o'chirish

**Endpoint:** `DELETE /api/subjects/{subject_id}`

**Vazifa:** Fanni o'chirish.

**Response:** `204 No Content`

**Xatoliklar:**
- `404 Not Found` - Fan topilmadi

---

### 3.4 Sinflarga biriktirilgan fanlar

**Endpoint:** `GET /api/subjects/grades`

**Vazifa:** Qaysi fan qaysi sinfda o'qitilishi va haftasiga necha soat.

**Response (200 OK):**
```json
[
  {
    "subject_id": 1,
    "grade": 5,
    "weekly_hours": 5,
    "name": "Matematika"
  },
  {
    "subject_id": 2,
    "grade": 7,
    "weekly_hours": 3,
    "name": "Fizika"
  }
]
```

---

### 3.5 Fanni sinfga biriktirish

**Endpoint:** `POST /api/subjects/grades`

**Vazifa:** Fanni ma'lum sinfga biriktirish va haftalik soatni belgilash.

**Request Body:**
```json
{
  "subject_id": 1,
  "grade": 5,
  "weekly_hours": 5
}
```

**Response (201 Created):**
```json
{
  "subject_id": 1,
  "grade": 5,
  "weekly_hours": 5,
  "name": "Matematika"
}
```

**Xatoliklar:**
- `404 Not Found` - Fan topilmadi
- `400 Bad Request` - Fan allaqachon shu sinfga biriktirilgan

---

### 3.6 Fan-sinf bog'liqligini o'chirish

**Endpoint:** `DELETE /api/subjects/grades/{subject_id}/{grade}`

**Vazifa:** Fanni sinfdan ajratish.

**Response:** `204 No Content`

**Xatoliklar:**
- `404 Not Found` - Bog'liq topilmadi

---

## 4. Sinflar (Classes)

Base: `/api/classes`
**🔒 Himoyalangan:** Barcha endpointlar access token talab qiladi

### 4.1 Barcha sinflarni olish

**Endpoint:** `GET /api/classes`

**Vazifa:** Barcha sinflar ro'yxatini olish.

**Response (200 OK):**
```json
[
  {
    "id": 1,
    "name": "5-A",
    "grade": 5,
    "section": "A",
    "student_count": 30,
    "class_teacher_id": 1
  }
]
```

---

### 4.2 Yangi sinf qo'shish

**Endpoint:** `POST /api/classes`

**Vazifa:** Yangi sinf qo'shish.

**Request Body:**
```json
{
  "name": "5-A",
  "grade": 5,
  "section": "A",
  "student_count": 30,
  "class_teacher_id": 1
}
```

**Response (201 Created):**
```json
{
  "id": 1,
  "name": "5-A",
  "grade": 5,
  "section": "A",
  "student_count": 30,
  "class_teacher_id": 1
}
```

**Xatoliklar:**
- `400 Bad Request` - Sinf allaqachon mavjud

---

### 4.3 Sinfni o'chirish

**Endpoint:** `DELETE /api/classes/{class_id}`

**Vazifa:** Sinfni o'chirish.

**Response:** `204 No Content`

**Xatoliklar:**
- `404 Not Found` - Sinf topilmadi

---

## 5. Xonalar (Rooms)

Base: `/api/rooms`
**🔒 Himoyalangan:** Barcha endpointlar access token talab qiladi

### 5.1 Barcha xonalarni olish

**Endpoint:** `GET /api/rooms`

**Vazifa:** Barcha dars xonalari ro'yxatini olish.

**Response (200 OK):**
```json
[
  {
    "id": 1,
    "name": "Xona 101",
    "capacity": 40
  },
  {
    "id": 2,
    "name": "Fizika kabineti",
    "capacity": 30
  }
]
```

---

### 5.2 Yangi xona qo'shish

**Endpoint:** `POST /api/rooms`

**Vazifa:** Yangi xona qo'shish.

**Request Body:**
```json
{
  "name": "Kimyo kabineti",
  "capacity": 35
}
```

**Response (201 Created):**
```json
{
  "id": 3,
  "name": "Kimyo kabineti",
  "capacity": 35
}
```

**Xatoliklar:**
- `400 Bad Request` - Xona allaqachon mavjud

---

### 5.3 Xonani o'chirish

**Endpoint:** `DELETE /api/rooms/{room_id}`

**Vazifa:** Xonani o'chirish.

**Response:** `204 No Content`

**Xatoliklar:**
- `404 Not Found` - Xona topilmadi

---

## 6. Dars Jadvali (Schedule)

Base: `/api/schedule`
**🔒 Himoyalangan:** Barcha endpointlar access token talab qiladi

### 6.1 Jadvalni olish

**Endpoint:** `GET /api/schedule`

**Vazifa:** Dars jadvali yozuvlarini olish (filter bilan yoki hammasi).

**Query Parameters:**
- `class_id` (ixtiyoriy): Sinf nomi (masalan: "5-A")
- `teacher_id` (ixtiyoriy): O'qituvchi ID

**Misollar:**
- `GET /api/schedule` - Barcha darslar
- `GET /api/schedule?class_id=5-A` - 5-A sinf jadvali
- `GET /api/schedule?teacher_id=3` - 3-ID o'qituvchi darslar

**Response (200 OK):**
```json
[
  {
    "id": 1,
    "class_id": "5-A",
    "teacher_id": 1,
    "subject_id": 1,
    "day": 0,
    "period": 1,
    "room": "Xona 101"
  }
]
```

**Kunlar:**
- `0` = Dushanba
- `1` = Seshanba
- `2` = Chorshanba
- `3` = Payshanba
- `4` = Juma
- `5` = Shanba

**Darslar:** `1-7` (birinchi darsdan ettinchigacha)

---

### 6.2 Yangi dars qo'shish

**Endpoint:** `POST /api/schedule`

**Vazifa:** Jadvalga yangi dars qo'shish (avtomatik konflikt tekshiruvi).

**Request Body:**
```json
{
  "class_id": "5-A",
  "teacher_id": 1,
  "subject_id": 1,
  "day": 0,
  "period": 1,
  "room": "Xona 101"
}
```

**Response (201 Created):**
```json
{
  "id": 1,
  "class_id": "5-A",
  "teacher_id": 1,
  "subject_id": 1,
  "day": 0,
  "period": 1,
  "room": "Xona 101"
}
```

**Xatoliklar:**
- `400 Bad Request` - Kun yoki dars raqami noto'g'ri
- `409 Conflict` - Sinf yoki o'qituvchi bu vaqtda band

**Konflikt misoli:**
```json
{
  "detail": "❌ Sinf konflikti: 5-A bu vaqtda allaqachon band!"
}
```

---

### 6.3 Darsni o'chirish

**Endpoint:** `DELETE /api/schedule/{entry_id}`

**Vazifa:** Jadvaldan darsni o'chirish.

**Response:** `204 No Content`

**Xatoliklar:**
- `404 Not Found` - Dars topilmadi

---

### 6.4 Konfliktlarni topish

**Endpoint:** `GET /api/schedule/conflicts`

**Vazifa:** Jadvaldagi barcha konfliktlarni topish.

**Response (200 OK):**
```json
[
  {
    "type": "class",
    "msg": "5-A sinfi Dushanba 1-darsda 2 ta dars: Matematika va Fizika"
  },
  {
    "type": "teacher",
    "msg": "Ahmadov Ali — Dushanba 2-darsda 5-A va 5-B da bir vaqtda"
  },
  {
    "type": "room",
    "msg": "Xona 101 — Seshanba 3-darsda 5-A va 6-A band"
  }
]
```

**Konflikt turlari:**
- `class` - Bir sinf bir vaqtda 2 ta darsda
- `teacher` - Bir o'qituvchi bir vaqtda 2 ta sinfda
- `room` - Bir xona bir vaqtda 2 ta sinf uchun

---

### 6.5 O'qituvchi almashtirishni topish

**Endpoint:** `GET /api/schedule/swap`

**Vazifa:** O'qituvchi kelmasa, uni kim almashtira olishini topish.

**Query Parameters:**
- `teacher_id` (majburiy): O'qituvchi ID
- `day` (majburiy): Kun (0-5)

**Misol:** `GET /api/schedule/swap?teacher_id=1&day=0`

**Response (200 OK):**
```json
[
  {
    "lesson_id": 1,
    "class_id": "5-A",
    "period": 1,
    "subject_id": 1,
    "subject_name": "Matematika",
    "possible": [
      {
        "id": 2,
        "name": "Karimova Malika"
      }
    ]
  }
]
```

**Xatoliklar:**
- `404 Not Found` - Bu kunda darsi yo'q

---

### 6.6 O'qituvchini almashtirish

**Endpoint:** `POST /api/schedule/swap`

**Vazifa:** Darsda o'qituvchini almashtirish.

**Request Body:**
```json
{
  "lesson_id": 1,
  "new_teacher_id": 2
}
```

**Response (200 OK):**
```json
{
  "id": 1,
  "class_id": "5-A",
  "teacher_id": 2,
  "subject_id": 1,
  "day": 0,
  "period": 1,
  "room": "Xona 101"
}
```

**Xatoliklar:**
- `404 Not Found` - Dars topilmadi
- `409 Conflict` - Yangi o'qituvchi bu vaqtda band

---

## 7. Hisobot (Report)

Base: `/api/report`
**🔒 Himoyalangan:** Access token talab qiladi

### 7.1 Jadval statistikasi

**Endpoint:** `GET /api/report`

**Vazifa:** Dars jadvali to'g'risida to'liq statistika va hisobot.

**Response (200 OK):**
```json
{
  "total_slots": 1260,
  "filled_slots": 450,
  "fill_percent": 36,
  "total_students": 900,
  "day_stats": [
    {
      "day": "Dushanba",
      "count": 75
    },
    {
      "day": "Seshanba",
      "count": 80
    }
  ],
  "subject_stats": [
    {
      "id": 1,
      "name": "Matematika",
      "count": 120,
      "teachers": 5
    },
    {
      "id": 2,
      "name": "Fizika",
      "count": 80,
      "teachers": 3
    }
  ]
}
```

**Ma'lumotlar:**
- `total_slots` - Jami dars joylari
- `filled_slots` - To'ldirilgan dars joylari
- `fill_percent` - To'ldirilish foizi
- `total_students` - Barcha o'quvchilar soni
- `day_stats` - Har kun uchun darslar soni
- `subject_stats` - Har fan uchun darslar va o'qituvchilar soni

---

## 8. Dashboard

**Endpoint:** `GET /api/dashboard`
**🔒 Himoyalangan:** Access token talab qiladi

**Vazifa:** Asosiy dashboard uchun umumiy ma'lumotlar.

**Response (200 OK):**
```json
{
  "teachers_count": 25,
  "subjects_count": 15,
  "lessons_count": 450,
  "classes_count": 30,
  "teacher_loads": [
    {
      "id": 1,
      "name": "Ahmadov Ali",
      "classes": ["5-A", "5-B", "6-A"],
      "weekly_lessons": 18
    }
  ]
}
```

---

## 🔒 Autentifikatsiya

Barcha himoyalangan endpointlar uchun **Bearer token** talab qilinadi.

**Header formatı:**
```
Authorization: Bearer <access_token>
```

**Misol:**
```bash
curl -H "Authorization: Bearer eyJhbGc..." http://localhost:8000/api/teachers
```

---

## ⚙️ Xatoliklar

### HTTP Status Kodlar:

- `200 OK` - Muvaffaqiyatli
- `201 Created` - Yaratildi
- `204 No Content` - O'chirildi (content yo'q)
- `400 Bad Request` - Noto'g'ri so'rov
- `401 Unauthorized` - Token yo'q yoki noto'g'ri
- `404 Not Found` - Topilmadi
- `409 Conflict` - Konflikt (masalan, sinf band)

### Xatolik formati:

```json
{
  "detail": "Xatolik xabari"
}
```

---

## 📝 Misollar

### Pythonda (requests):

```python
import requests

# Login
response = requests.post("http://localhost:8000/api/auth/login", json={
    "username": "admin",
    "password": "admin123"
})
tokens = response.json()
access_token = tokens["access_token"]

# O'qituvchilar ro'yxati
headers = {"Authorization": f"Bearer {access_token}"}
teachers = requests.get("http://localhost:8000/api/teachers", headers=headers)
print(teachers.json())
```

### JavaScriptda (fetch):

```javascript
// Login
const loginRes = await fetch('http://localhost:8000/api/auth/login', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ username: 'admin', password: 'admin123' })
});
const { access_token } = await loginRes.json();

// O'qituvchilar ro'yxati
const teachersRes = await fetch('http://localhost:8000/api/teachers', {
  headers: { 'Authorization': `Bearer ${access_token}` }
});
const teachers = await teachersRes.json();
console.log(teachers);
```

### cURL:

```bash
# Login
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin123"}'

# O'qituvchilar (tokenni almashtiring)
curl http://localhost:8000/api/teachers \
  -H "Authorization: Bearer <your_token_here>"
```

---

## 🚀 Production Deployment

### Environment Variables (.env):

```bash
# Database
DATABASE_URL=postgresql://user:password@host:5432/dbname

# JWT Security (MUHIM: O'zgartiring!)
SECRET_KEY=your-very-secure-random-key-here
REFRESH_SECRET_KEY=your-refresh-secure-random-key-here

# Admin
ADMIN_USERNAME=admin
ADMIN_PASSWORD=very-strong-password-here
```

### Xavfsizlik Tavsiyalar:

1. `.env` fayldagi barcha kalitlarni o'zgartiring
2. HTTPS ishlatilishiga ishonch hosil qiling
3. Production database parolini kuchli qiling
4. CORS sozlamalarini cheklang (hozir `allow_origins=["*"]`)
5. Rate limiting qo'shing (DDoS himoya)

---

## 📞 Qo'llab-quvvatlash

**API Versiya:** 1.0.0
**Framework:** FastAPI
**Database:** PostgreSQL
**Authentication:** JWT (Access + Refresh tokens)

---

**© 2026 EduPlan - Maktab dars jadvali tizimi**