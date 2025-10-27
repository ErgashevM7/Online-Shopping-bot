# import sqlite3
# from sqlite3 import Error

# DB_NAME = "maxsulot.db"

# def init_db():
#     conn = sqlite3.connect(DB_NAME)
#     cur = conn.cursor()
#     # products table (sening ustun nomlariga mos)
#     cur.execute("""
#         CREATE TABLE IF NOT EXISTS maxsulot (
#             id INTEGER PRIMARY KEY,
#             maxsulot TEXT,
#             price INTEGER,
#             image TEXT,
#             dec TEXT
#         )
#     """)
#     # cart table
#     cur.execute("""
#         CREATE TABLE IF NOT EXISTS karzinka (
#             id INTEGER PRIMARY KEY AUTOINCREMENT,
#             user_id INTEGER,
#             product_id INTEGER,
#             product_name TEXT,
#             total_price INTEGER,
#             count INTEGER
#         )
#     """)
#     conn.commit()
#     conn.close()

# def get_products():
#     conn = sqlite3.connect(DB_NAME)
#     cur = conn.cursor()
#     cur.execute("SELECT id, maxsulot, price, image, dec FROM maxsulot")
#     rows = cur.fetchall()
#     conn.close()
#     return rows

# def get_product_by_id(product_id):
#     conn = sqlite3.connect(DB_NAME)
#     cur = conn.cursor()
#     cur.execute("SELECT id, maxsulot, price, image, dec FROM maxsulot WHERE id=?", (product_id,))
#     row = cur.fetchone()
#     conn.close()
#     return row

# def add_to_cart(user_id, product_id, product_name, total_price, count):
#     conn = sqlite3.connect(DB_NAME)
#     cur = conn.cursor()
#     cur.execute("""
#         INSERT INTO karzinka(user_id, product_id, product_name, total_price, count)
#         VALUES (?, ?, ?, ?, ?)
#     """, (user_id, product_id, product_name, total_price, count))
#     conn.commit()
#     conn.close()

# def get_cart(user_id):
#     conn = sqlite3.connect(DB_NAME)
#     cur = conn.cursor()
#     cur.execute("SELECT * FROM karzinka WHERE user_id=?", (user_id,))
#     rows = cur.fetchall()
#     conn.close()
#     return rows

# def clear_cart(user_id):
#     conn = sqlite3.connect(DB_NAME)
#     cur = conn.cursor()
#     cur.execute("DELETE FROM karzinka WHERE user_id=?", (user_id,))
#     conn.commit()
#     conn.close()






import sqlite3
import os

# Fayl yo‘lini aniq qilib olish
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_NAME = os.path.join(BASE_DIR, "maxsulot.db")

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS maxsulot (
            id INTEGER PRIMARY KEY,
            maxsulot TEXT,
            price INTEGER,
            image TEXT,
            dec TEXT
        )
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS karzinka (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            product_id INTEGER,
            product_name TEXT,
            total_price INTEGER,
            count INTEGER
        )
    """)
    conn.commit()
    conn.close()


def get_products():
    conn = sqlite3.connect("maxsulot.db")
    cur = conn.cursor()
    cur.execute("SELECT id, maxsulot, price, image, dec FROM products")
    products = cur.fetchall()
    conn.close()
    return products

# def get_products():
#     conn = sqlite3.connect(DB_NAME)
#     cur = conn.cursor()
#     cur.execute("SELECT id, maxsulot, price, image, dec FROM maxsulot")
#     rows = cur.fetchall()
#     conn.close()
#     return rows

def get_product_by_id(product_id):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("SELECT id, maxsulot, price, image, dec FROM maxsulot WHERE id=?", (product_id,))
    row = cur.fetchone()
    conn.close()
    return row

def add_to_cart(user_id, product_id, product_name, total_price, count):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO karzinka(user_id, product_id, product_name, total_price, count)
        VALUES (?, ?, ?, ?, ?)
    """, (user_id, product_id, product_name, total_price, count))
    conn.commit()
    conn.close()

def get_cart(user_id):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("SELECT * FROM karzinka WHERE user_id=?", (user_id,))
    rows = cur.fetchall()
    conn.close()
    return rows

def clear_cart(user_id):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("DELETE FROM karzinka WHERE user_id=?", (user_id,))
    conn.commit()
    conn.close()
# print("Bazaga ulanmoqda:", DB_NAME)

def test_products():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM maxsulot")
    count = cur.fetchone()[0]
    conn.close()
    # print(f" Bazada {count} ta mahsulot bor")







def add_product(name, price, image, desc):
    conn = sqlite3.connect("maxsulot.db")
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO products (maxsulot, price, image, dec)
        VALUES (?, ?, ?, ?)
    """, (name, price, image, desc))
    conn.commit()
    conn.close()