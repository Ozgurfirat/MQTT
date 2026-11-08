import tkinter as tk
from tkinter import ttk, messagebox
from translate import Translator  # Yeni hafif kütüphane


class CeviriUygulamasi:
    def __init__(self, root):
        self.root = root
        self.root.title("Python Kolay Çeviri")
        self.root.geometry("550x450")
        self.root.configure(bg="#f0f2f5")
        self.arayuz_tasarla()

    def arayuz_tasarla(self):
        baslik = tk.Label(self.root, text="Masaüstü Çeviri Programı", font=("Arial", 16, "bold"), bg="#f0f2f5",
                          fg="#1a73e8")
        baslik.pack(pady=10)

        dil_cercevesi = tk.Frame(self.root, bg="#f0f2f5")
        dil_cercevesi.pack(pady=5)

        tk.Label(dil_cercevesi, text="Kaynak Dil:", font=("Arial", 10), bg="#f0f2f5").grid(row=0, column=0, padx=5)
        self.kaynak_dil_cb = ttk.Combobox(dil_cercevesi, values=["Türkçe", "İngilizce"], width=12, state="readonly")
        self.kaynak_dil_cb.grid(row=0, column=1, padx=5)
        self.kaynak_dil_cb.set("Türkçe")

        degis_btn = tk.Button(dil_cercevesi, text="⇄", font=("Arial", 12, "bold"), bg="#ffffff", fg="#5f6368",
                              command=self.dilleri_degistir, relief="groove")
        degis_btn.grid(row=0, column=2, padx=10)

        tk.Label(dil_cercevesi, text="Hedef Dil:", font=("Arial", 10), bg="#f0f2f5").grid(row=0, column=3, padx=5)
        self.hedef_dil_cb = ttk.Combobox(dil_cercevesi, values=["Türkçe", "İngilizce"], width=12, state="readonly")
        self.hedef_dil_cb.grid(row=0, column=4, padx=5)
        self.hedef_dil_cb.set("İngilizce")

        tk.Label(self.root, text="Çevrilecek Metin:", font=("Arial", 11, "bold"), bg="#f0f2f5", fg="#3c4043").pack(
            anchor="w", padx=25, pady=(10, 2))
        self.giris_metni = tk.Text(self.root, height=5, width=60, font=("Arial", 11), wrap="word", bd=2,
                                   relief="groove")
        self.giris_metni.pack(padx=25, fill="x")

        self.cevir_btn = tk.Button(self.root, text="Çevir", font=("Arial", 12, "bold"), bg="#1a73e8", fg="white",
                                   command=self.metni_cevir, cursor="hand2")
        self.cevir_btn.pack(pady=15, ipady=3, ipadx=20)

        tk.Label(self.root, text="Çeviri Sonucu:", font=("Arial", 11, "bold"), bg="#f0f2f5", fg="#3c4043").pack(
            anchor="w", padx=25, pady=(5, 2))
        self.sonuc_metni = tk.Text(self.root, height=5, width=60, font=("Arial", 11), wrap="word", bg="#f8f9fa", bd=2,
                                   relief="groove", state="disabled")
        self.sonuc_metni.pack(padx=25, fill="x")

    def dilleri_degistir(self):
        kaynak = self.kaynak_dil_cb.get()
        hedef = self.hedef_dil_cb.get()
        self.kaynak_dil_cb.set(hedef)
        self.hedef_dil_cb.set(kaynak)

    def metni_cevir(self):
        orijinal_metin = self.giris_metni.get("1.0", tk.END).strip()
        if not orijinal_metin:
            messagebox.showwarning("Uyarı", "Lütfen çevirmek istediğiniz bir metin girin.")
            return

        dil_haritasi = {"Türkçe": "tr", "İngilizce": "en"}
        src_lang = dil_haritasi[self.kaynak_dil_cb.get()]
        dest_lang = dil_haritasi[self.hedef_dil_cb.get()]

        try:
            # translate kütüphanesi motoru
            translator = Translator(from_lang=src_lang, to_lang=dest_lang)
            cevirilen_metin = translator.translate(orijinal_metin)

            self.sonuc_metni.config(state="normal")
            self.sonuc_metni.delete("1.0", tk.END)
            self.sonuc_metni.insert(tk.END, cevirilen_metin)
            self.sonuc_metni.config(state="disabled")
            self.sonuc_metni.config(state="disabled")
        except Exception as e:
            messagebox.showerror("Hata", f"Çeviri başarısız oldu.\nHata: {e}")


if __name__ == "__main__":
    pencere = tk.Tk()
    uygulama = CeviriUygulamasi(pencere)
    pencere.mainloop()
