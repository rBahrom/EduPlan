"""
EduPlan — Namuna maktab ma'lumoti (seed data).

O'zbekiston umumiy o'rta ta'lim maktablari o'quv rejasi (5–11 sinf) asosida:
- Barcha fanlar (qiyinligi va afzal vaqti bilan)
- Qaysi fan qaysi sinfga, haftasiga necha soat
- Sinflar (5-A ... 11-B), xonalar (oddiy + amaliy fan laboratoriyalari), o'qituvchilar

Bu fayl YAGONA manba: ham `POST /api/seed` endpoint, ham `seed.sql` eksporti
shu yerdagi ma'lumotni ishlatadi (takrorlanish bo'lmasligi uchun).
"""

# ─── FANLAR ───────────────────────────────────────────────────────────────────
# (nom, qiyinlik 1–5, afzal_vaqt "morning"/"any", amaliy_xona_kerakmi)
# difficulty: og'ir fanlar (mat, fizika) tushlikkacha joylashtiriladi.
# practical=True bo'lgan fanlarga generator alohida laboratoriya beradi.
SUBJECTS = [
    # nom,                    difficulty, preferred_time, practical
    ("Ona tili",                  4, "morning", False),
    ("Adabiyot",                  3, "any",     False),
    ("Matematika",                5, "morning", False),
    ("Algebra",                   5, "morning", False),
    ("Geometriya",                5, "morning", False),
    ("Fizika",                    5, "morning", True),
    ("Kimyo",                     5, "morning", True),
    ("Biologiya",                 4, "morning", True),
    ("Geografiya",                3, "any",     False),
    ("Tarix",                     3, "any",     False),
    ("O'zbekiston tarixi",        3, "any",     False),
    ("Jahon tarixi",              3, "any",     False),
    ("Ingliz tili",               4, "any",     False),
    ("Rus tili",                  3, "any",     False),
    ("Informatika",               4, "any",     True),
    ("Tarbiya",                   2, "any",     False),
    ("Jismoniy tarbiya",          2, "any",     True),
    ("Chizmachilik",              3, "any",     False),
    ("Tasviriy san'at",           2, "any",     False),
    ("Musiqa",                    2, "any",     True),
    ("Texnologiya",               2, "any",     True),
    ("Iqtisodiy bilim asoslari",  3, "any",     False),
    ("Huquq",                     3, "any",     False),
]

# Amaliy (laboratoriya/maxsus xona) talab qiladigan fanlar — yuqoridagi practical=True
PRACTICAL_SUBJECTS = {name for name, _, _, practical in SUBJECTS if practical}


# ─── SINF-FAN-SOAT REJASI ─────────────────────────────────────────────────────
# Har sinf darajasi (5–11) uchun: {fan_nomi: haftalik_soat}
# O'zbekiston tayanch o'quv rejasiga yaqinlashtirilgan namuna.
CURRICULUM = {
    5: {
        "Ona tili": 4, "Adabiyot": 2, "Matematika": 5, "Ingliz tili": 3,
        "Rus tili": 2, "Tarix": 2, "Geografiya": 2, "Biologiya": 2,
        "Informatika": 1, "Tasviriy san'at": 1, "Musiqa": 1,
        "Jismoniy tarbiya": 3, "Texnologiya": 2, "Tarbiya": 1,
    },
    6: {
        "Ona tili": 3, "Adabiyot": 2, "Matematika": 5, "Ingliz tili": 3,
        "Rus tili": 2, "Tarix": 2, "Geografiya": 2, "Biologiya": 2,
        "Informatika": 1, "Tasviriy san'at": 1, "Musiqa": 1,
        "Jismoniy tarbiya": 3, "Texnologiya": 2, "Tarbiya": 1,
    },
    7: {
        "Ona tili": 3, "Adabiyot": 2, "Algebra": 3, "Geometriya": 2,
        "Fizika": 2, "Ingliz tili": 3, "Rus tili": 2, "Tarix": 2,
        "Geografiya": 2, "Biologiya": 2, "Informatika": 1, "Chizmachilik": 1,
        "Jismoniy tarbiya": 3, "Texnologiya": 2, "Tarbiya": 1,
    },
    8: {
        "Ona tili": 2, "Adabiyot": 2, "Algebra": 3, "Geometriya": 2,
        "Fizika": 2, "Kimyo": 2, "Ingliz tili": 3, "Rus tili": 2,
        "Tarix": 2, "Geografiya": 2, "Biologiya": 2, "Informatika": 1,
        "Chizmachilik": 1, "Jismoniy tarbiya": 3, "Tarbiya": 1,
    },
    9: {
        "Ona tili": 2, "Adabiyot": 3, "Algebra": 3, "Geometriya": 2,
        "Fizika": 3, "Kimyo": 2, "Ingliz tili": 3, "Rus tili": 2,
        "O'zbekiston tarixi": 2, "Jahon tarixi": 1, "Geografiya": 2,
        "Biologiya": 2, "Informatika": 2, "Jismoniy tarbiya": 3,
    },
    10: {
        "Ona tili": 2, "Adabiyot": 3, "Algebra": 3, "Geometriya": 2,
        "Fizika": 3, "Kimyo": 2, "Ingliz tili": 3, "Rus tili": 2,
        "O'zbekiston tarixi": 2, "Jahon tarixi": 1, "Geografiya": 1,
        "Biologiya": 2, "Informatika": 2, "Jismoniy tarbiya": 2,
        "Iqtisodiy bilim asoslari": 1, "Huquq": 1,
    },
    11: {
        "Ona tili": 2, "Adabiyot": 3, "Algebra": 3, "Geometriya": 2,
        "Fizika": 3, "Kimyo": 2, "Ingliz tili": 3, "Rus tili": 2,
        "O'zbekiston tarixi": 2, "Jahon tarixi": 1, "Biologiya": 2,
        "Informatika": 2, "Jismoniy tarbiya": 2,
        "Iqtisodiy bilim asoslari": 1, "Huquq": 1,
    },
}


# ─── SINFLAR ──────────────────────────────────────────────────────────────────
# 5-A ... 11-B (har darajada 2 ta parallel). Hammasi 1-smena (keyin o'zgartiriladi).
GRADES = [5, 6, 7, 8, 9, 10, 11]
SECTIONS = ["A", "B"]


def build_classes():
    """Sinflar ro'yxati: (name, grade, section, student_count, shift)."""
    classes = []
    for g in GRADES:
        for s in SECTIONS:
            classes.append((f"{g}-{s}", g, s, 30, 1))
    return classes


# ─── XONALAR ──────────────────────────────────────────────────────────────────
# 1) Har sinf uchun bitta oddiy xona (sinf xonasi).
# 2) Amaliy fanlar uchun alohida maxsus xonalar (laboratoriya/zal/ustaxona).
SPECIAL_ROOMS = [
    # nom,                          sig'imi
    ("Fizika laboratoriyasi",          30),
    ("Kimyo laboratoriyasi",           30),
    ("Biologiya laboratoriyasi",       30),
    ("Informatika xonasi 1",           24),
    ("Informatika xonasi 2",           24),
    ("Sport zali",                     60),
    ("Musiqa xonasi",                  30),
    ("Texnologiya ustaxonasi (o'g'il)",25),
    ("Texnologiya xonasi (qiz)",       25),
]


def build_rooms():
    """Xonalar: (name, capacity). Har sinfga 1 ta oddiy + maxsus laboratoriyalar."""
    rooms = []
    # Har sinf uchun oddiy xona (raqamlangan): 101, 102, ...
    n = 101
    for g in GRADES:
        for s in SECTIONS:
            rooms.append((f"{n}-xona ({g}-{s})", 30))
            n += 1
    # Maxsus (amaliy fan) xonalari
    rooms.extend(SPECIAL_ROOMS)
    return rooms


# ─── O'QITUVCHILAR ────────────────────────────────────────────────────────────
# Fan o'qituvchilari — har biriga o'qitadigan fan(lar)i biriktirilgan.
# (name, phone, [fan nomlari]) — fan nomlari SUBJECTS dagi nomlarga mos bo'lishi shart.
# Sinflarga (qaysi sinfga dars beradi) biriktirish foydalanuvchi tomonidan keyin qilinadi.
TEACHERS = [
    ("Aziza Karimova",        "+998901112201", ["Ona tili", "Adabiyot"]),
    ("Dilnoza Yusupova",      "+998901112202", ["Ona tili", "Adabiyot"]),
    ("Bahrom Rashidov",       "+998901112203", ["Matematika", "Algebra"]),
    ("Sardor Aliyev",         "+998901112204", ["Matematika", "Geometriya"]),
    ("Gulnora Tosheva",       "+998901112205", ["Algebra", "Geometriya"]),
    ("Jasur Ergashev",        "+998901112206", ["Fizika"]),
    ("Nodira Saidova",        "+998901112207", ["Kimyo"]),
    ("Feruza Qodirova",       "+998901112208", ["Biologiya"]),
    ("Otabek Nazarov",        "+998901112209", ["Geografiya"]),
    ("Malika Umarova",        "+998901112210", ["Tarix", "O'zbekiston tarixi", "Jahon tarixi"]),
    ("Shahzod Kamolov",       "+998901112211", ["Ingliz tili"]),
    ("Kamola Ismoilova",      "+998901112212", ["Ingliz tili"]),
    ("Elena Petrova",         "+998901112213", ["Rus tili"]),
    ("Ulug'bek Tursunov",     "+998901112214", ["Informatika"]),
    ("Zarina Hakimova",       "+998901112215", ["Informatika"]),
    ("Rustam Qosimov",        "+998901112216", ["Jismoniy tarbiya"]),
    ("Laziz Mahmudov",        "+998901112217", ["Jismoniy tarbiya"]),
    ("Sevara Abdullayeva",    "+998901112218", ["Musiqa", "Tasviriy san'at"]),
    ("Bekzod Sobirov",        "+998901112219", ["Texnologiya", "Chizmachilik"]),
    ("Mehriniso Yo'ldosheva", "+998901112220", ["Tarbiya", "Huquq", "Iqtisodiy bilim asoslari"]),
]


# ─── SINF RAHBARLARI ──────────────────────────────────────────────────────────
# Har sinfga bittadan rahbar. Kalit = sinf nomi, qiymat = o'qituvchi ismi
# (TEACHERS dagi nomga mos). 14 sinf, 20 o'qituvchi — har biri ko'pi bilan 1 sinf rahbari.
CLASS_TEACHERS = {
    "5-A":  "Aziza Karimova",
    "5-B":  "Dilnoza Yusupova",
    "6-A":  "Bahrom Rashidov",
    "6-B":  "Sardor Aliyev",
    "7-A":  "Gulnora Tosheva",
    "7-B":  "Jasur Ergashev",
    "8-A":  "Nodira Saidova",
    "8-B":  "Feruza Qodirova",
    "9-A":  "Otabek Nazarov",
    "9-B":  "Malika Umarova",
    "10-A": "Shahzod Kamolov",
    "10-B": "Kamola Ismoilova",
    "11-A": "Elena Petrova",
    "11-B": "Ulug'bek Tursunov",
}
