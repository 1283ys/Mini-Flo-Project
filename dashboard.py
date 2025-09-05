import sqlite3
from tkinter import *
from tkinter import ttk, messagebox
from listings import list_magazalar, list_calisanlar, list_urunler 

conn = sqlite3.connect("main.db")
cur = conn.cursor()

cur.execute("""
    CREATE TABLE IF NOT EXISTS magaza (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        sehir TEXT NOT NULL,
        isim TEXT NOT NULL,    
        tur TEXT CHECK(tur IN ('Yurt İçi','Yurt Dışı')) NOT NULL
    )
""")

cur.execute("""
    CREATE TABLE IF NOT EXISTS calisan (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        isim TEXT NOT NULL,
        tur TEXT CHECK(tur IN ('Full Time','Part Time')) NOT NULL,
        magaza_id INTEGER NOT NULL,
        FOREIGN KEY (magaza_id) REFERENCES magaza(id)
    )
""")

cur.execute("""
    CREATE TABLE IF NOT EXISTS urun (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        isim TEXT NOT NULL,
        kategori TEXT CHECK(kategori IN ('Giyim','Ayakkabı','Aksesuar')) NOT NULL,
        stok INTEGER NOT NULL,
        magaza_id INTEGER NOT NULL,
        FOREIGN KEY (magaza_id) REFERENCES magaza(id)
    )
""")

conn.commit()


def magaza_ekle_form():
    win = Toplevel()
    win.title("Mağaza Ekle")

    Label(win, text="Şehir:").pack()
    sehir_entry = Entry(win)
    sehir_entry.pack()

    Label(win, text="İsim:").pack()
    isim_entry = Entry(win)
    isim_entry.pack()

    Label(win, text="Tür:").pack()
    tur_var = StringVar()
    tur_combo = ttk.Combobox(win, textvariable=tur_var, values=["Yurt İçi","Yurt Dışı"])
    tur_combo.pack()

    def kaydet():
        sehir = sehir_entry.get()
        isim = isim_entry.get()
        tur = tur_var.get()
        if sehir and isim and tur:
            cur.execute("INSERT INTO magaza (sehir,isim,tur) VALUES (?,?,?)", (sehir,isim,tur))
            conn.commit()
            messagebox.showinfo("Başarılı","Mağaza eklendi!")
            win.destroy()
        else:
            messagebox.showerror("Hata","Lütfen tüm alanları doldurun!")

    Button(win, text="Kaydet", command=kaydet).pack()


def calisan_ekle_form():
    win = Toplevel()
    win.title("Çalışan Ekle")

    Label(win, text="İsim:").pack()
    isim_entry = Entry(win)
    isim_entry.pack()

    Label(win, text="Çalışma Türü:").pack()
    tur_var = StringVar()
    tur_combo = ttk.Combobox(win, textvariable=tur_var, values=["Full Time","Part Time"])
    tur_combo.pack()

    Label(win, text="Mağaza:").pack()
    cur.execute("SELECT id, isim FROM magaza")
    magaza_list = cur.fetchall()
    magaza_dict = {f"{isim} (ID:{id})": id for id, isim in magaza_list}
    magaza_var = StringVar()
    magaza_combo = ttk.Combobox(win, textvariable=magaza_var, values=list(magaza_dict.keys()))
    magaza_combo.pack()

    def kaydet():
        isim = isim_entry.get()
        tur = tur_var.get()
        secilen = magaza_var.get()
        if isim and tur and secilen:
            magaza_id = magaza_dict[secilen]
            cur.execute("INSERT INTO calisan (isim,tur,magaza_id) VALUES (?,?,?)",
                        (isim,tur,magaza_id))  
            conn.commit()
            messagebox.showinfo("Başarılı","Çalışan eklendi!")
            win.destroy()
        else:
            messagebox.showerror("Hata","Lütfen tüm alanları doldurun!")

    Button(win, text="Kaydet", command=kaydet).pack()


def urun_ekle_form():
    win = Toplevel()
    win.title("Ürün Ekle")

    Label(win, text="Ürün İsmi:").pack()
    isim_entry = Entry(win)
    isim_entry.pack()

    Label(win, text="Kategori:").pack()
    kategori_var = StringVar()
    kategori_combo = ttk.Combobox(win, textvariable=kategori_var, values=["Giyim","Ayakkabı","Aksesuar"])
    kategori_combo.pack()

    Label(win, text="Stok Adedi:").pack()
    stok_entry = Entry(win)
    stok_entry.pack()

    Label(win, text="Mağaza:").pack()
    cur.execute("SELECT id, isim FROM magaza")
    magaza_list = cur.fetchall()
    magaza_dict = {f"{isim} (ID:{id})": id for id, isim in magaza_list}
    magaza_var = StringVar()
    magaza_combo = ttk.Combobox(win, textvariable=magaza_var, values=list(magaza_dict.keys()))
    magaza_combo.pack()

    def kaydet():
        isim = isim_entry.get()
        kategori = kategori_var.get()
        stok = stok_entry.get()
        secilen = magaza_var.get()

        if isim and kategori and stok.isdigit() and secilen:
            magaza_id = magaza_dict[secilen]
            cur.execute("INSERT INTO urun (isim,kategori,stok,magaza_id) VALUES (?,?,?,?)",
                        (isim, kategori, int(stok), magaza_id))
            conn.commit()
            messagebox.showinfo("Başarılı","Ürün eklendi!")
            win.destroy()
        else:
            messagebox.showerror("Hata","Lütfen tüm alanları doğru doldurun!")

    Button(win, text="Kaydet", command=kaydet).pack()


def open_dashboard(root, username):
    for widget in root.winfo_children():
        widget.destroy()

    Label(root, text=f"Hoşgeldin {username}!", font=("Arial",16)).pack(pady=20)

    Button(root, text="Mağaza Ekle", command=magaza_ekle_form, width=20).pack(pady=10)
    Button(root, text="Çalışan Ekle", command=calisan_ekle_form, width=20).pack(pady=10)
    Button(root, text="Ürün Ekle", command=urun_ekle_form, width=20).pack(pady=10)
    Button(root, text="Mağazaları Listele", width=20, command=list_magazalar).pack(pady=10)
    Button(root, text="Çalışanları Listele", width=20, command=list_calisanlar).pack(pady=10)
    Button(root, text="Ürünleri Listele", width=20, command=list_urunler).pack(pady=10)