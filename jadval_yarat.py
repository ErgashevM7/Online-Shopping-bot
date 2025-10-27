import sqlite3
conn = sqlite3.connect("maxsulot.db")
cursor = conn.cursor()


cursor.execute("""
CREATE TABLE IF NOT EXISTS maxsulot (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    maxsulot TEXT NOT NULL,
    price REAL NOT NULL,
    image TEXT NOT NULL,
    dec TEXT NOT NULL
)
""")


cursor.execute("""
INSERT OR IGNORE INTO maxsulot (maxsulot,price, image, dec)
VALUES (?, ?, ?, ?)
""", ("Kadi", 5000, "https://data.daryo.uz/media/2023/Sevara/tykva.jpg", "Elotni kadisi"))


conn.commit()
conn.close()

print("✅ Database yaratildi va ma'lumot qo'shildi!")
