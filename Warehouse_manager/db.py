import sqlite3

def get_connection():
    return sqlite3.connect("warehouse.db")

def init_db():
    with get_connection() as conn:
        c = conn.cursor()
        c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            username TEXT UNIQUE,
            password TEXT
        )
        """)
        c.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY,
            name TEXT,
            quantity INTEGER
        )
        """)
        c.execute('''
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                quantity INTEGER NOT NULL
            )
        ''')
        # Kiểm tra xem cột 'group_name' có tồn tại không
        c.execute("PRAGMA table_info(products)")
        columns = [col[1] for col in c.fetchall()]
        if "group_name" not in columns:
            c.execute("ALTER TABLE products ADD COLUMN group_name TEXT")

        conn.commit()