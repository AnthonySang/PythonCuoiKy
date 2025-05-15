import sqlite3

conn = sqlite3.connect("warehouse.db")  # tên file CSDL của bạn
c = conn.cursor()

# Thêm cột role nếu chưa có
try:
    c.execute("ALTER TABLE users ADD COLUMN role TEXT DEFAULT 'user'")
    print("✅ Đã thêm cột 'role' thành công.")
except sqlite3.OperationalError as e:
    print("⚠️ Cột 'role' đã tồn tại hoặc lỗi khác:", e)

conn.commit()
conn.close()
