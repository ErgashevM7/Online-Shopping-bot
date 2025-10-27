import sqlite3
import os

DB_PATH = r"c:\Karzinka 2 bot\maxsulot.db"

# 🔧 Agar baza mavjud bo'lmasa, xabar beramiz
if not os.path.exists(DB_PATH):
    print(f"❌ Fayl topilmadi: {DB_PATH}")
else:
    print(f"✅ Baza topildi: {DB_PATH}")

conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

# 🔄 Jadval borligini tekshiramiz
cur.execute("""
    CREATE TABLE IF NOT EXISTS maxsulot (
        id INTEGER PRIMARY KEY,
        maxsulot TEXT,
        price INTEGER,
        image TEXT,
        dec TEXT
    )
""")

# 🔽 Mahsulotlar ro‘yxati
products = [
    (1, 'Gashir', 9000, 'https://storage.kun.uz/source/7/T4OBdj_L7BP211xfQ4gJB2sHpIyU4htC.jpg', 'Svejiy sabzilar'),
    (2, 'Shaftoli', 9000, 'https://klau.club/uploads/posts/2023-06/1685644994_klau-club-p-shaftoli-1.jpg', 'Chotki shaftoli'),
    (3, 'Olma', 5000, 'https://upload.wikimedia.org/wikipedia/commons/thumb/1/15/Red_Apple.jpg/1200px-Red_Apple.jpg', 'Imod ogomni bog‘idan olma'),
    (4, 'Banan', 12000, 'https://xs.uz/upload/post/2020/09/14/86f3ce58168a3beef82450601469f91a0914.jpg', 'Afrika bananlari'),
    (5, 'Ananas', 50000, 'https://stat.uz/images/ananas-1--kopiya.jpg', 'Afrika ananasi'),
    (6, 'Kadi', 5000, 'https://data.daryo.uz/media/2023/Sevara/tykva.jpg', 'Elotni kadisi')
]

# 🔁 Eski ma'lumotlarni o'chirib, yangilarni kiritamiz
cur.execute("DELETE FROM maxsulot")
cur.executemany("INSERT INTO maxsulot VALUES (?, ?, ?, ?, ?)", products)
conn.commit()
conn.close()

print("✅ 6 ta mahsulot muvaffaqiyatli qo‘shildi!")
