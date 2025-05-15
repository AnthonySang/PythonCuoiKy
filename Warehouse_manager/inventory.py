import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import db
import openpyxl

def open_inventory():
    def add_product():
        name = name_entry.get().strip()
        qty = qty_entry.get().strip()
        group = group_entry.get().strip()

        if not name or not qty.isdigit():
            messagebox.showwarning("Lỗi", "Vui lòng nhập tên, số lượng và nhóm hàng hợp lệ.")
            return

        with db.get_connection() as conn:
            c = conn.cursor()
            c.execute("INSERT INTO products (name, quantity, group_name) VALUES (?, ?, ?)", (name, int(qty), group))
            conn.commit()

        name_entry.delete(0, tk.END)
        qty_entry.delete(0, tk.END)
        group_entry.delete(0, tk.END)
        update_list()

    def update_list(filter_text=""):
        for i in tree.get_children():
            tree.delete(i)

        with db.get_connection() as conn:
            c = conn.cursor()
            if filter_text:
                c.execute("SELECT id, name, quantity, group_name FROM products WHERE name LIKE ?", ('%' + filter_text + '%',))
            else:
                c.execute("SELECT id, name, quantity, group_name FROM products")
            for row in c.fetchall():
                tree.insert("", tk.END, values=row)

    def on_search(event=None):
        filter_text = search_entry.get().strip()
        update_list(filter_text)

    def delete_product():
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Thông báo", "Vui lòng chọn một sản phẩm để xoá.")
            return

        item = tree.item(selected)
        product_id = item['values'][0]

        confirm = messagebox.askyesno("Xác nhận", "Bạn có chắc chắn muốn xoá sản phẩm này?")
        if confirm:
            with db.get_connection() as conn:
                c = conn.cursor()
                c.execute("DELETE FROM products WHERE id=?", (product_id,))
                conn.commit()
            update_list()

    def update_quantity():
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Thông báo", "Vui lòng chọn một sản phẩm để cập nhật.")
            return

        item = tree.item(selected)
        product_id = item['values'][0]

        new_qty = simple_input("Nhập số lượng mới:", "Cập nhật số lượng")
        if new_qty is not None and new_qty.isdigit():
            with db.get_connection() as conn:
                c = conn.cursor()
                c.execute("UPDATE products SET quantity=? WHERE id=?", (int(new_qty), product_id))
                conn.commit()
            update_list()

    def edit_product():
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Thông báo", "Vui lòng chọn một sản phẩm để sửa tên.")
            return

        item = tree.item(selected)
        product_id = item['values'][0]
        current_name = item['values'][1]

        new_name = simple_input(f"Tên hiện tại: {current_name}\nNhập tên mới:", "Sửa tên sản phẩm")
        if new_name and new_name.strip():
            with db.get_connection() as conn:
                c = conn.cursor()
                c.execute("UPDATE products SET name=? WHERE id=?", (new_name.strip(), product_id))
                conn.commit()
            update_list()

    def simple_input(prompt, title):
        popup = tk.Toplevel()
        popup.title(title)
        popup.geometry("250x120")
        popup.grab_set()

        tk.Label(popup, text=prompt).pack(pady=5)
        entry = tk.Entry(popup)
        entry.pack(pady=5)

        value = []

        def submit():
            value.append(entry.get())
            popup.destroy()

        tk.Button(popup, text="OK", command=submit).pack(pady=5)
        popup.wait_window()
        return value[0] if value else None

    def export_excel():
        path = filedialog.asksaveasfilename(defaultextension=".xlsx",
                                             filetypes=[("Excel Files", "*.xlsx")],
                                             title="Lưu báo cáo kho")

        if not path:
            return

        workbook = openpyxl.Workbook()
        sheet = workbook.active
        sheet.title = "Báo cáo kho"

        sheet.append(["ID", "Tên sản phẩm", "Số lượng", "Nhóm hàng"])
        for item in tree.get_children():
            row = tree.item(item)["values"]
            sheet.append(row)

        try:
            workbook.save(path)
            messagebox.showinfo("Thành công", f"Báo cáo đã được lưu: {path}")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể lưu file: {e}")

    # Tạo cửa sổ chính
    win = tk.Toplevel()
    win.title("Quản lý kho")

    window_width = 750
    window_height = 550
    screen_width = win.winfo_screenwidth()
    screen_height = win.winfo_screenheight()
    x = (screen_width - window_width) // 2
    y = (screen_height - window_height) // 2
    win.geometry(f"{window_width}x{window_height}+{x}+{y}")

    # Tiêu đề
    tk.Label(win, text="📦 QUẢN LÝ KHO", font=("Arial", 20, "bold")).pack(pady=15)

    # Form nhập liệu
    form_frame = tk.Frame(win)
    form_frame.pack()

    tk.Label(form_frame, text="📝 Tên sản phẩm:", font=("Arial", 12)).grid(row=0, column=0, padx=10, pady=5)
    name_entry = tk.Entry(form_frame, font=("Arial", 12), width=30)
    name_entry.grid(row=0, column=1)

    tk.Label(form_frame, text="🔢 Số lượng:", font=("Arial", 12)).grid(row=1, column=0, padx=10, pady=5)
    qty_entry = tk.Entry(form_frame, font=("Arial", 12), width=30)
    qty_entry.grid(row=1, column=1)

    tk.Label(form_frame, text="📂 Nhóm hàng:", font=("Arial", 12)).grid(row=2, column=0, padx=10, pady=5)
    group_entry = tk.Entry(form_frame, font=("Arial", 12), width=30)
    group_entry.grid(row=2, column=1)

    tk.Button(form_frame, text="➕ Thêm sản phẩm", font=("Arial", 12), bg="#4CAF50", fg="white",
              command=add_product).grid(row=3, column=0, columnspan=2, pady=10)

    # Tìm kiếm
    search_frame = tk.Frame(win)
    search_frame.pack(anchor='ne', padx=20, pady=5)

    tk.Label(search_frame, text="🔎", font=("Arial", 14)).pack(side=tk.LEFT)
    search_entry = tk.Entry(search_frame, font=("Arial", 11), width=20)
    search_entry.pack(side=tk.LEFT, padx=5)
    search_entry.bind("<Return>", on_search)
    tk.Button(search_frame, text="Tìm", font=("Arial", 11), command=on_search).pack(side=tk.LEFT, padx=5)

    # Bảng dữ liệu
    tree = ttk.Treeview(win, columns=("ID", "Tên", "Số lượng", "Nhóm"), show="headings")
    tree.heading("ID", text="🆔 ID")
    tree.heading("Tên", text="📄 Tên sản phẩm")
    tree.heading("Số lượng", text="📦 Số lượng")
    tree.heading("Nhóm", text="📂 Nhóm hàng")

    tree.column("ID", width=50, anchor="center")
    tree.column("Tên", width=220)
    tree.column("Số lượng", width=100, anchor="center")
    tree.column("Nhóm", width=150, anchor="center")

    style = ttk.Style()
    style.configure("Treeview.Heading", font=("Arial", 12, "bold"))
    style.configure("Treeview", font=("Arial", 11))
    tree.pack(fill=tk.BOTH, expand=True, pady=10, padx=20)

    # Nút chức năng
    btn_frame = tk.Frame(win)
    btn_frame.pack(pady=10)

    tk.Button(btn_frame, text="🗑️ Xoá sản phẩm", font=("Arial", 12), bg="#f44336", fg="white", command=delete_product).pack(side=tk.LEFT, padx=10)
    tk.Button(btn_frame, text="✏️ Sửa sản phẩm", font=("Arial", 12), bg="#FF9800", fg="white", command=edit_product).pack(side=tk.LEFT, padx=10)
    tk.Button(btn_frame, text="🔁 Cập nhật số lượng", font=("Arial", 12), bg="#2196F3", fg="white", command=update_quantity).pack(side=tk.LEFT, padx=10)
    tk.Button(btn_frame, text="📄 Xuất Excel", font=("Arial", 12), bg="#9C27B0", fg="white", command=export_excel).pack(side=tk.LEFT, padx=10)

    update_list()
