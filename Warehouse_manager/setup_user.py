import db

with db.get_connection() as conn:
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username=?", ("Vansang",))
    if not c.fetchone():
        c.execute("INSERT INTO users (username, password) VALUES (?, ?)", ("Vansang", "123"))
        conn.commit()
        print("✅ Tài khoản admin đã được tạo.")
    else:
        print("ℹ️ Tài khoản 'admin' đã tồn tại.")
