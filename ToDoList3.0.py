import tkinter as tk
from tkinter import messagebox, ttk
from datetime import datetime
import json
import os

DOSYA_ADI = "gorevler.json"

class ToDoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("📝 Gelişmiş Yapılacaklar Listesi")
        self.root.geometry("600x650")

        self.gorevler = []
        self.kategoriler = ["İş", "Kişisel", "Diğer"]
        self.temalar = {
            "Koyu": {
                "bg": "#000435", "fg": "#ffffff",
                "entry_bg": "#1e1e4f", "entry_fg": "#ffffff",
                "listbox_bg": "#1e1e4f", "listbox_fg": "#ffffff"
            },
            "Aydınlık": {
                "bg": "#ffffff", "fg": "#000000",
                "entry_bg": "#ffffff", "entry_fg": "#000000",
                "listbox_bg": "#ffffff", "listbox_fg": "#000000"
            }
        }
        self.tema = "Aydınlık"  # Varsayılan tema

        self.baslik = tk.Label(root, text="Yapılacaklar Listesi", font=("Helvetica", 16, "bold"))
        self.baslik.pack(pady=10)

        self.gorev_frame = tk.Frame(root)
        self.gorev_frame.pack()

        self.entry_gorev = tk.Entry(self.gorev_frame, width=30, font=("Helvetica", 12))
        self.entry_gorev.grid(row=0, column=0, padx=5)

        self.kategori_sec = ttk.Combobox(self.gorev_frame, values=self.kategoriler, state="readonly", width=12)
        self.kategori_sec.grid(row=0, column=1)
        self.kategori_sec.set("İş")

        self.ekle_btn = tk.Button(self.gorev_frame, text="➕ Ekle", command=self.gorev_ekle)
        self.ekle_btn.grid(row=0, column=2, padx=5)

        self.arama_entry = tk.Entry(root, width=40)
        self.arama_entry.pack(pady=5)
        self.arama_entry.insert(0, "Görev ara...")
        self.arama_entry.bind("<KeyRelease>", self.gorev_ara)

        self.kategori_filtresi = ttk.Combobox(root, values=["Tümü"] + self.kategoriler, state="readonly")
        self.kategori_filtresi.pack(pady=5)
        self.kategori_filtresi.set("Tümü")
        self.kategori_filtresi.bind("<<ComboboxSelected>>", lambda e: self.gorevleri_guncelle())

        self.liste = tk.Listbox(root, width=70, height=15, font=("Courier", 10))
        self.liste.pack(pady=10)

        self.islem_frame = tk.Frame(root)
        self.islem_frame.pack()

        self.tamamla_btn = tk.Button(self.islem_frame, text="✔️ Tamamlandı", width=15, command=self.tamamla)
        self.tamamla_btn.grid(row=0, column=0, padx=5)

        self.sil_btn = tk.Button(self.islem_frame, text="🗑️ Sil", width=15, command=self.sil)
        self.sil_btn.grid(row=0, column=1, padx=5)

        self.kaydet_btn = tk.Button(root, text="💾 Kaydet", command=self.kaydet)
        self.kaydet_btn.pack(pady=5)

        self.tema_buton = tk.Button(root, text="🌗 Tema Değiştir", command=self.tema_degistir)
        self.tema_buton.pack(pady=5)

        self.temayi_uygula()
        self.gorevleri_yukle()

    def tema_degistir(self):
        self.tema = "Aydınlık" if self.tema == "Koyu" else "Koyu"
        self.temayi_uygula()

    def temayi_uygula(self):
        t = self.temalar[self.tema]
        self.root.config(bg=t["bg"])
        self.baslik.config(bg=t["bg"], fg=t["fg"])
        self.gorev_frame.config(bg=t["bg"])
        self.entry_gorev.config(bg=t["entry_bg"], fg=t["entry_fg"])
        self.kategori_sec.config(background=t["entry_bg"], foreground=t["entry_fg"])
        self.arama_entry.config(bg=t["entry_bg"], fg=t["entry_fg"])
        self.kategori_filtresi.config(background=t["entry_bg"], foreground=t["entry_fg"])
        self.liste.config(bg=t["listbox_bg"], fg=t["listbox_fg"])
        self.islem_frame.config(bg=t["bg"])
        self.ekle_btn.config(bg=t["entry_bg"], fg=t["fg"])
        self.sil_btn.config(bg=t["entry_bg"], fg=t["fg"])
        self.tamamla_btn.config(bg=t["entry_bg"], fg=t["fg"])
        self.kaydet_btn.config(bg=t["entry_bg"], fg=t["fg"])
        self.tema_buton.config(bg=t["entry_bg"], fg=t["fg"])

    def gorev_ekle(self):
        ad = self.entry_gorev.get().strip()
        kategori = self.kategori_sec.get()
        if ad == "":
            messagebox.showwarning("Uyarı", "Görev adı boş olamaz.")
            return
        yeni = {
            "ad": ad,
            "kategori": kategori,
            "tarih": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "tamamlandi": False
        }
        self.gorevler.append(yeni)
        self.entry_gorev.delete(0, tk.END)
        self.gorevleri_guncelle()

    def gorevleri_guncelle(self):
        arama = self.arama_entry.get().lower().strip()
        kategori_filtre = self.kategori_filtresi.get()
        self.liste.delete(0, tk.END)

        for g in self.gorevler:
            if (arama in g["ad"].lower() or arama == "" or arama == "görev ara...") and \
               (kategori_filtre == "Tümü" or g["kategori"] == kategori_filtre):
                etiket = "✔️ " if g["tamamlandi"] else ""
                goster = f"{etiket}{g['ad']} | {g['kategori']} | {g['tarih']}"
                self.liste.insert(tk.END, goster)

    def gorev_ara(self, event):
        self.gorevleri_guncelle()

    def tamamla(self):
        secilen = self.liste.curselection()
        if not secilen:
            return
        gosterilen_text = self.liste.get(secilen[0])
        for g in self.gorevler:
            if g["ad"] in gosterilen_text:
                g["tamamlandi"] = True
                break
        self.gorevleri_guncelle()

    def sil(self):
        secilen = self.liste.curselection()
        if not secilen:
            return
        gosterilen_text = self.liste.get(secilen[0])
        for g in self.gorevler:
            if g["ad"] in gosterilen_text:
                self.gorevler.remove(g)
                break
        self.gorevleri_guncelle()

    def kaydet(self):
        try:
            with open(DOSYA_ADI, "w", encoding="utf-8") as f:
                json.dump(self.gorevler, f, ensure_ascii=False, indent=4)
            messagebox.showinfo("Başarılı", "Görevler kaydedildi.")
        except Exception as e:
            messagebox.showerror("Hata", f"Kaydetme hatası: {str(e)}")

    def gorevleri_yukle(self):
        if os.path.exists(DOSYA_ADI):
            try:
                with open(DOSYA_ADI, "r", encoding="utf-8") as f:
                    self.gorevler = json.load(f)
                    self.gorevleri_guncelle()
            except Exception as e:
                messagebox.showerror("Yükleme Hatası", str(e))

if __name__ == "__main__":
    root = tk.Tk()
    app = ToDoApp(root)
    root.mainloop()
