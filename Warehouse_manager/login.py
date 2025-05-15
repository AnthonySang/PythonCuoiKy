import customtkinter as ctk
import tkinter as tk
import dashboard
import db
from tkinter import messagebox
from PIL import Image, ImageTk


def login_window():
    def check_login(event=None):
        username = user_entry.get()
        password = pass_entry.get()

        with db.get_connection() as conn:
            c = conn.cursor()
            c.execute("SELECT username, role FROM users WHERE username=? AND password=?", (username, password))
            result = c.fetchone()
            if result:
                root.destroy()
                dashboard.open_dashboard(result[0], result[1])
            else:
                messagebox.showerror("Lỗi", "❌ Sai tên đăng nhập hoặc mật khẩu.")

    ctk.set_appearance_mode("light")  # "dark" or "system"
    ctk.set_default_color_theme("blue")

    root = ctk.CTk()
    root.geometry("500x400")
    root.title("🔐 Đăng nhập hệ thống")
    
    #// Load và hiển thị hình nền
    #bg_image = Image.open("qlk.jpg")
    #bg_image = bg_image.resize((500, 350))
    #bg_photo = ImageTk.PhotoImage(bg_image)
    #bg_label = tk.Label(root, image=bg_photo)
    #bg_label.place(x=0, y=0, relwidth=1, relheight=1)

    # Avatar
    avatar_image = Image.open("game.png")  # file ảnh 
    avatar_image = avatar_image.resize((100, 100))
    avatar_photo = ImageTk.PhotoImage(avatar_image)
    avatar_label = ctk.CTkLabel(master=root, image=avatar_photo, text="")
    avatar_label.pack(pady=10)

    # Tiêu đề
    ctk.CTkLabel(root, text="QUẢN LÝ KHO", font=ctk.CTkFont(size=20, weight="bold")).pack(pady=10)

    user_entry = ctk.CTkEntry(root, placeholder_text="👤 Tài khoản")
    user_entry.pack(pady=10)

    pass_entry = ctk.CTkEntry(root, placeholder_text="🔒 Mật khẩu", show="*")
    pass_entry.pack(pady=10)

    login_btn = ctk.CTkButton(root, text="➡️ Đăng nhập", command=check_login)
    login_btn.pack(pady=20)

    # Hỗ trợ Enter
    root.bind("<Return>", check_login)

    root.mainloop()
