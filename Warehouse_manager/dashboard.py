import tkinter as tk
import inventory
import report  # Đảm bảo bạn đã có file report.py

def open_dashboard(username, role="user"):
    root = tk.Tk()
    root.title("📦 Hệ thống quản lý kho")
    root.resizable(False, False)

    # Căn giữa
    width, height = 500, 400
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2
    root.geometry(f"{width}x{height}+{x}+{y}")
    root.configure(bg="#ffffff")

    # Thông tin người dùng
    info_frame = tk.Frame(root, bg="#ffffff")
    info_frame.pack(anchor='ne', padx=10, pady=5)
    avatar = "🧑‍💼" if role != "admin" else "👑"
    tk.Label(info_frame, text=f"{avatar} {username} ({role})", font=("Arial", 11, "italic"), bg="#ffffff", fg="#444").pack(anchor='ne')

    # Tiêu đề
    tk.Label(root, text="📦 QUẢN LÝ KHO HÀNG", font=("Arial", 20, "bold"), fg="#222", bg="#ffffff").pack(pady=15)

    # Khung nút
    btn_frame = tk.Frame(root, bg="#ffffff")
    btn_frame.pack(pady=15)

    def styled_button(text, color, cmd):
        return tk.Button(btn_frame, text=text, font=("Arial", 14), width=25, height=2,
                         bg=color, fg="white", relief=tk.FLAT, command=cmd)

    styled_button("📦 Quản lý kho", "#4CAF50", inventory.open_inventory).pack(pady=10)
    styled_button("📊 Báo cáo thống kê", "#2196F3", report.generate_filtered_report).pack(pady=10)
    styled_button("🚪 Thoát", "#f44336", root.destroy).pack(pady=10)

    root.mainloop()
