import tkinter as tk
from tkinter import messagebox
import sqlite3
from dashboard import open_dashboard
from listings import list_magazalar, list_calisanlar, list_urunler   
DB_PATH = "login.db"

def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL
            )
        """)
        cur.execute("SELECT COUNT(*) FROM users")
        (count,) = cur.fetchone()
        if count == 0:
            cur.execute(
                "INSERT INTO users (username, password) VALUES (?, ?)",
                ("admin", "1234")
            )
        conn.commit()

def login():
    u = entry_username.get().strip()
    p = entry_password.get()
    if not u or not p:
        messagebox.showwarning("Uyarı", "Kullanıcı adı ve şifre boş olamaz.")
        return
    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.cursor()
        cur.execute(
            "SELECT id FROM users WHERE username=? AND password=?",
            (u, p)
        )
        row = cur.fetchone()
    if row:
        entry_password.delete(0, tk.END)
        open_dashboard(root, u) 
    else:
        messagebox.showerror("Hata", "Kullanıcı adı veya şifre hatalı.")

def register_user():
    u = entry_username.get().strip()
    p = entry_password.get()
    if not u or not p:
        messagebox.showwarning("Uyarı", "Kullanıcı adı ve şifre boş olamaz.")
        return
    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.cursor()
        try:
            cur.execute(
                "INSERT INTO users (username, password) VALUES (?, ?)",
                (u, p)
            )
            conn.commit()
            messagebox.showinfo("Başarılı", f"'{u}' kullanıcısı eklendi.")
        except sqlite3.IntegrityError:
            messagebox.showerror("Hata", "Bu kullanıcı adı zaten kayıtlı.")

def toggle_pw():
    entry_password.config(show="" if var_show.get() else "*")

root = tk.Tk()
root.title("Mini Flo Takip Sistemi")
root.geometry("700x600")
root.resizable(False, False)
root.configure(bg="#ff6600") 


tk.Label(
    root,
    text="Mini Flo Takip Sistemine Hoşgeldiniz",
    font=("Arial", 16, "bold"),
    bg="#ff6600",
    fg="white"
).pack(pady=30)


frm = tk.Frame(root, bg="white", padx=30, pady=30, relief="ridge", bd=3)
frm.pack(pady=40)


tk.Label(frm, text="Kullanıcı Adı:", font=("Arial", 12, "bold"), bg="white", fg="black").grid(row=0, column=0, sticky="e", padx=8, pady=8)
entry_username = tk.Entry(frm, width=30, font=("Arial", 12))
entry_username.grid(row=0, column=1, pady=8)


tk.Label(frm, text="Şifre:", font=("Arial", 12, "bold"), bg="white", fg="black").grid(row=1, column=0, sticky="e", padx=8, pady=8)
entry_password = tk.Entry(frm, width=30, font=("Arial", 12), show="*")
entry_password.grid(row=1, column=1, pady=8)


var_show = tk.BooleanVar(value=False)
tk.Checkbutton(frm, text="Şifreyi Göster", variable=var_show, command=toggle_pw, bg="white").grid(row=2, column=1, sticky="w", pady=6)


btns = tk.Frame(root, bg="#ff6600")
btns.pack(pady=20)

tk.Button(btns, text="Giriş Yap", width=16, font=("Arial", 11, "bold"), bg="black", fg="white", activebackground="#333333", activeforeground="white", command=login).grid(row=0, column=0, padx=10)
tk.Button(btns, text="Yeni Kullanıcı Ekle", width=18, font=("Arial", 11, "bold"), bg="white", fg="black", activebackground="#ff944d", activeforeground="black", command=register_user).grid(row=0, column=1, padx=10)

init_db()
root.mainloop()
