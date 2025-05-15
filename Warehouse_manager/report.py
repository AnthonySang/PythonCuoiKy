import sqlite3
from tkinter import *
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from db import get_connection  # Hàm này nên return sqlite3.connect("ten_database.db")
from reportlab.pdfgen import canvas
import matplotlib.pyplot as plt


def generate_filtered_report():
    def export_pdf(data):
        c = canvas.Canvas("bao_cao_kho.pdf")
        c.setFont("Helvetica-Bold", 14)
        c.drawString(200, 800, "📦 BÁO CÁO KHO HÀNG")

        c.setFont("Helvetica", 10)
        y = 760
        c.drawString(40, y, "Tên sản phẩm")
        c.drawString(200, y, "Số lượng")
        c.drawString(300, y, "Nhóm")
        c.drawString(400, y, "Ngày nhập")

        y -= 20
        for row in data:
            c.drawString(40, y, str(row[0]))
            c.drawString(200, y, str(row[1]))
            c.drawString(300, y, str(row[2]))
            c.drawString(400, y, str(row[3]))
            y -= 20

        c.save()
        messagebox.showinfo("Xuất PDF", "Đã lưu file báo cáo PDF thành công!")

    def show_pie_chart(data):
        chart_data = {}
        for row in data:
            nhom = row[2]  # nhóm hàng
            soluong = int(row[1])
            chart_data[nhom] = chart_data.get(nhom, 0) + soluong

        if not chart_data:
            messagebox.showinfo("Thông báo", "Không có dữ liệu để vẽ biểu đồ.")
            return

        labels = list(chart_data.keys())
        sizes = list(chart_data.values())

        plt.figure(figsize=(6, 6))
        plt.pie(sizes, labels=labels, autopct="%1.1f%%", startangle=90)
        plt.title("📊 Biểu đồ số lượng theo nhóm hàng")
        plt.axis("equal")
        plt.show()

    def apply_filter():
        ten = ten_entry.get()
        nhom = nhom_entry.get()
        date = date_entry.get_date()

        query = "SELECT ten, soluong, nhom, ngaynhap FROM kho WHERE 1=1"
        params = []

        if ten:
            query += " AND ten LIKE ?"
            params.append(f"%{ten}%")
        if nhom:
            query += " AND nhom LIKE ?"
            params.append(f"%{nhom}%")
        if date:
            query += " AND ngaynhap = ?"
            params.append(date.strftime('%Y-%m-%d'))

        with get_connection() as conn:
            cur = conn.cursor()
            cur.execute(query, params)
            rows = cur.fetchall()

        # Xóa bảng cũ
        for i in tree.get_children():
            tree.delete(i)

        # Hiển thị bảng mới
        for row in rows:
            tree.insert("", END, values=row)

        # Gán nút PDF và vẽ biểu đồ
        btn_pdf.config(command=lambda: export_pdf(rows))
        show_pie_chart(rows)

    # Giao diện bộ lọc
    win = Toplevel()
    win.title("🔎 Bộ lọc & Báo cáo kho")
    win.geometry("700x550")
    win.configure(bg="#f5f5f5")

    Label(win, text="Tên sản phẩm:", bg="#f5f5f5").place(x=20, y=20)
    ten_entry = Entry(win, width=25)
    ten_entry.place(x=150, y=20)

    Label(win, text="Nhóm hàng:", bg="#f5f5f5").place(x=20, y=60)
    nhom_entry = Entry(win, width=25)
    nhom_entry.place(x=150, y=60)

    Label(win, text="Ngày nhập:", bg="#f5f5f5").place(x=20, y=100)
    date_entry = DateEntry(win, width=22, background='darkblue',
                           foreground='white', borderwidth=2)
    date_entry.place(x=150, y=100)

    Button(win, text="🔍 Lọc dữ liệu", bg="#4CAF50", fg="white",
           width=15, command=apply_filter).place(x=150, y=140)

    btn_pdf = Button(win, text="📄 Xuất PDF", bg="#2196F3", fg="white", width=15)
    btn_pdf.place(x=300, y=140)

    # Bảng kết quả
    cols = ("Tên sản phẩm", "Số lượng", "Nhóm", "Ngày nhập")
    tree = ttk.Treeview(win, columns=cols, show="headings", height=12)
    for col in cols:
        tree.heading(col, text=col)
        tree.column(col, anchor="center")
    tree.place(x=20, y=200, width=650)

    # Đường kẻ cuộn
    scrollbar = ttk.Scrollbar(win, orient="vertical", command=tree.yview)
    scrollbar.place(x=670, y=200, height=260)
    tree.configure(yscrollcommand=scrollbar.set)
