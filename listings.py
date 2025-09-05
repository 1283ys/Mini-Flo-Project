import tkinter as tk
from tkinter import ttk, simpledialog , messagebox
import sqlite3

DB_PATH = "main.db"

def list_magazalar():
    win = tk.Toplevel()
    win.title("Mağaza Listesi")
    win.geometry("600x300")

    tree = ttk.Treeview(win, columns=("id", "isim", "sehir", "tur"), show="headings")
    tree.heading("id", text="ID")
    tree.heading("isim", text="İsim")
    tree.heading("sehir", text="Şehir")
    tree.heading("tur", text="Tür")

    tree.column("id", width=40, anchor="center")
    tree.column("isim", width=150)
    tree.column("sehir", width=120)
    tree.column("tur", width=100)

    tree.pack(fill="both", expand=True)

    scrollbar = ttk.Scrollbar(win, orient="vertical", command=tree.yview)
    tree.configure(yscroll=scrollbar.set)
    scrollbar.pack(side="right", fill="y")

    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.cursor()
        cur.execute("SELECT id, isim, sehir, tur FROM magaza")
        rows = cur.fetchall()
        for row in rows:
            tree.insert("", "end", values=row)

   
def list_calisanlar():
    win = tk.Toplevel()
    win.title("Çalışan Listesi")
    win.geometry("600x300")

    tree = ttk.Treeview(win, columns=("id", "isim", "tur", "magaza_id"), show="headings")
    tree.heading("id", text="ID")
    tree.heading("isim", text="İsim")
    tree.heading("tur", text="Tür")
    tree.heading("magaza_id", text="Mağaza ID")

    tree.column("id", width=40, anchor="center")
    tree.column("isim", width=150)
    tree.column("tur", width=120)
    tree.column("magaza_id", width=100)

    tree.pack(fill="both", expand=True)

    scrollbar = ttk.Scrollbar(win, orient="vertical", command=tree.yview)
    tree.configure(yscroll=scrollbar.set)
    scrollbar.pack(side="right", fill="y")

    def calisan_sil():
        selected = tree.selection()
        if not selected:
            tk.messagebox.showwarning("Uyarı", "Silmek için bir çalışan seçin.")
            return
        item = tree.item(selected[0])
        calisan_id = item["values"][0]

        with sqlite3.connect(DB_PATH) as conn:
            cur = conn.cursor()
            cur.execute("DELETE FROM calisan WHERE id=?", (calisan_id,))
            conn.commit()

        tree.delete(selected[0])
        tk.messagebox.showinfo("Başarılı", "Çalışan silindi.")

    btn = tk.Button(win, text="Seçili Çalışanı Sil", command=calisan_sil, bg="red", fg="white")
    btn.pack(pady=5)

    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.cursor()
        cur.execute("SELECT id, isim, tur, magaza_id FROM calisan")
        rows = cur.fetchall()
        for row in rows:
            tree.insert("", "end", values=row)


def list_urunler():
    win = tk.Toplevel()
    win.title("Ürün Listesi")
    win.geometry("600x300")

    tree = ttk.Treeview(win, columns=("id", "isim", "kategori", "stok", "magaza_id"), show="headings")
    tree.heading("id", text="ID")
    tree.heading("isim", text="İsim")
    tree.heading("kategori", text="Kategori")
    tree.heading("stok", text="Stok")
    tree.heading("magaza_id", text="Mağaza ID")

    tree.column("id", width=40, anchor="center")
    tree.column("isim", width=150)
    tree.column("kategori", width=120)
    tree.column("stok", width=100, anchor="center")
    tree.column("magaza_id", width=100)

    tree.pack(fill="both", expand=True)

    scrollbar = ttk.Scrollbar(win, orient="vertical", command=tree.yview)
    tree.configure(yscroll=scrollbar.set)
    scrollbar.pack(side="right", fill="y")

    def urun_sil():
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Uyarı", "Silmek için bir ürün seçin.")
            return

        item = tree.item(selected[0])
        urun_id, isim, kategori, stok, magaza_id = item["values"]

        adet = simpledialog.askinteger("Stok Azalt", f"{isim} ürününden kaç adet silmek istiyorsunuz?",
                                    minvalue=1, maxvalue=stok)

        if adet is None:
            return  

        with sqlite3.connect(DB_PATH) as conn:
            cur = conn.cursor()
            if adet < stok:
                yeni_stok = stok - adet
                cur.execute("UPDATE urun SET stok=? WHERE id=?", (yeni_stok, urun_id))
                conn.commit()
                messagebox.showinfo("Başarılı", f"{isim} ürününden {adet} adet silindi. Yeni stok: {yeni_stok}")
                tree.item(selected[0], values=(urun_id, isim, kategori, yeni_stok, magaza_id))
            else:
                cur.execute("DELETE FROM urun WHERE id=?", (urun_id,))
                conn.commit()
                tree.delete(selected[0])
                messagebox.showinfo("Başarılı", f"{isim} ürünü tamamen silindi.")

    btn = tk.Button(win, text="Seçili Ürünü Sil", command=urun_sil, bg="red", fg="white")
    btn.pack(pady=5)

    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.cursor()
        cur.execute("SELECT id, isim, kategori, stok, magaza_id FROM urun")
        rows = cur.fetchall()
        for row in rows:
            tree.insert("", "end", values=row)




    