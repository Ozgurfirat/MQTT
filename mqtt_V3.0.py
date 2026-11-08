import tkinter as tk
from tkinter import messagebox, ttk
import paho.mqtt.client as mqtt




class MQTTApp:

  def __init__(self, root):
    self.root = root
    self.root.title("Modern MQTT Kontrol Paneli")
    self.root.geometry("1150x720")
    self.root.config(bg="#f4f6f9")

    # Değişkenler
    self.bağlantı_değişkeni = tk.StringVar(value="test.mosquitto.org")
    self.abone_değişkeni = tk.StringVar()
    self.yayın_başlığı = ""

    # Renk Paleti ve Fontlar
    self.BG_COLOR = "#f4f6f9"
    self.CARD_BG = "#ffffff"
    self.TEXT_COLOR = "#2c3e50"
    self.PRIMARY_COLOR = "#3498db"
    self.PRIMARY_HOVER = "#2980b9"
    self.SUCCESS_COLOR = "#2ecc71"
    self.SUCCESS_HOVER = "#27ae60"
    self.DANGER_COLOR = "#e74c3c"
    self.DANGER_HOVER = "#c0392b"
    self.FONT_MAIN = ("Segoe UI", 11, "bold")
    self.FONT_TITLE = ("Segoe UI", 12, "bold")
    self.FONT_TEXT = ("Consolas", 11)

    # MQTT İstemci Tanımlamaları
    self.client = mqtt.Client()
    self.client.on_message = self.mesaj_alındı
    self.client.on_connect = self.bağlantı_sağlandı

    # Arayüzü Oluştur ve Bağlan
    self._arayüzü_oluştur()
    self._mqtt_başlat()

  def _arayüzü_oluştur(self):
    style = ttk.Style()
    style.theme_use("clam")

    # __________________ GELEN VERİ BÖLÜMÜ __________________
    gelen_etiketi = tk.Label(
        self.root,
        font=self.FONT_TITLE,
        text="GELEN VERİ",
        bg=self.BG_COLOR,
        fg=self.TEXT_COLOR,
    )
    gelen_etiketi.grid(row=0, column=0, padx=15, pady=(15, 5), sticky="w")

    self.gelen_yazı_kutusu = tk.Text(
        self.root,
        font=self.FONT_TEXT,
        width=32,
        height=13,
        bd=2,
        relief="groove",
        bg="#ffffff",
        fg="#333333",
    )
    self.gelen_yazı_kutusu.grid(
        row=1, column=0, padx=15, pady=5, rowspan=2, sticky="nsew"
    )

    # __________________ GÖNDERİLEN VERİ BÖLÜMÜ __________________
    gönderilen_etiketi = tk.Label(
        self.root,
        font=self.FONT_TITLE,
        text="GÖNDERİLEN VERİ",
        bg=self.BG_COLOR,
        fg=self.TEXT_COLOR,
    )
    gönderilen_etiketi.grid(row=0, column=1, padx=15, pady=(15, 5), sticky="w")

    self.gönderilen_yazı_kutusu = tk.Text(
        self.root,
        font=self.FONT_TEXT,
        width=32,
        height=13,
        bd=2,
        relief="groove",
        bg="#ffffff",
        fg="#333333",
    )
    self.gönderilen_yazı_kutusu.grid(
        row=1, column=1, padx=15, pady=5, rowspan=2, sticky="nsew"
    )

    # __________________ BAŞLIK ETİKETLERİ & GİRİŞLER __________________
    abone_yazısı = tk.Label(
        self.root,
        font=self.FONT_MAIN,
        text="ABONE BAŞLIĞI",
        bg=self.BG_COLOR,
        fg=self.TEXT_COLOR,
    )
    abone_yazısı.grid(row=3, column=0, padx=15, pady=(10, 0), sticky="w")

    yayınlama_yazısı = tk.Label(
        self.root,
        font=self.FONT_MAIN,
        text="YAYINLAMA BAŞLIĞI",
        bg=self.BG_COLOR,
        fg=self.TEXT_COLOR,
    )
    yayınlama_yazısı.grid(row=3, column=1, padx=15, pady=(10, 0), sticky="w")

    self.abone_giriş = tk.Entry(
        self.root, font=self.FONT_MAIN, bd=2, relief="solid"
    )
    self.abone_giriş.grid(
        row=4, column=0, padx=15, pady=5, ipady=4, sticky="ew"
    )

    self.yayın_giriş = tk.Entry(
        self.root, font=self.FONT_MAIN, bd=2, relief="solid"
    )
    self.yayın_giriş.grid(
        row=4, column=1, padx=15, pady=5, ipady=4, sticky="ew"
    )

    self.abone_onay_tuşu = self._modern_buton(
        self.root,
        "Abone Ol",
        self.SUCCESS_COLOR,
        self.SUCCESS_HOVER,
        self.abone_ol,
    )
    self.abone_onay_tuşu.grid(row=5, column=0, padx=15, pady=10, sticky="ew")

    self.yayın_onay_tuşu = self._modern_buton(
        self.root,
        "Yayın Onayla",
        self.PRIMARY_COLOR,
        self.PRIMARY_HOVER,
        self.yayın_başlığı_güncelle,
    )
    self.yayın_onay_tuşu.grid(row=5, column=1, padx=15, pady=10, sticky="ew")

    # __________________ BAĞLANTI İŞLEMLERİ ÇERÇEVESİ __________________
    bağlantı_çerçevesi = tk.LabelFrame(
        self.root,
        text=" BAĞLANTI İŞLEMLERİ ",
        font=self.FONT_TITLE,
        bg=self.CARD_BG,
        fg=self.TEXT_COLOR,
        bd=2,
        relief="groove",
        padx=10,
        pady=10,
    )
    bağlantı_çerçevesi.grid(
        row=1, column=2, padx=15, pady=5, sticky="nsew", rowspan=2
    )

    bağlantı_adresleri = [
        "test.mosquitto.org",
        "broker.hivemq.com",
        "broker.emqx.io",
    ]
    self.bağlantı_combobox = ttk.Combobox(
        bağlantı_çerçevesi,
        textvariable=self.bağlantı_değişkeni,
        width=25,
        font=self.FONT_MAIN,
    )
    self.bağlantı_combobox.grid(row=1, column=0, padx=10, pady=10)
    self.bağlantı_combobox["values"] = bağlantı_adresleri

    self.bağlan_tuşu = self._modern_buton(
        bağlantı_çerçevesi,
        "BAĞLAN",
        self.PRIMARY_COLOR,
        self.PRIMARY_HOVER,
        self.bağlan,
    )
    self.bağlan_tuşu.grid(row=2, column=0, padx=10, pady=10, sticky="ew")

    self.mesaj_gönder_tuşu = self._modern_buton(
        self.root,
        "MESAJ\nGÖNDER",
        self.SUCCESS_COLOR,
        self.SUCCESS_HOVER,
        self.mesaj_yolla,
    )
    self.mesaj_gönder_tuşu.grid(row=3, column=2, padx=15, pady=10, sticky="ew")

    # __________________ ABONELİK İŞLEMLERİ ÇERÇEVESİ __________________
    abone_çerçevesi = tk.LabelFrame(
        self.root,
        text=" ABONELİK İŞLEMLERİ ",
        font=self.FONT_TITLE,
        bg=self.CARD_BG,
        fg=self.TEXT_COLOR,
        bd=2,
        relief="groove",
        padx=10,
        pady=10,
    )
    abone_çerçevesi.grid(
        row=4, column=2, padx=15, pady=5, sticky="nsew", rowspan=2
    )

    self.abone_combobox = ttk.Combobox(
        abone_çerçevesi,
        textvariable=self.abone_değişkeni,
        width=25,
        font=self.FONT_MAIN,
    )
    self.abone_combobox.grid(
        row=1, column=0, padx=10, pady=10, columnspan=2, sticky="ew"
    )
    self.abone_combobox["values"] = []

    self.abone_ol_tuşu = self._modern_buton(
        abone_çerçevesi,
        "Abone Ol",
        self.SUCCESS_COLOR,
        self.SUCCESS_HOVER,
        self.abone_ol,
    )
    self.abone_ol_tuşu.grid(row=2, column=0, padx=5, pady=10, sticky="ew")

    self.abonelikten_çık_tuşu = self._modern_buton(
        abone_çerçevesi,
        "Abonelikten\nÇık",
        self.DANGER_COLOR,
        self.DANGER_HOVER,
        self.abonelikten_çık,
    )
    self.abonelikten_çık_tuşu.grid(row=2, column=1, padx=5, pady=10, sticky="ew")

  # Dinamik Hover (Üzerine Gelme) Efektli Buton Üreteci
  def _modern_buton(self, parent, text, bg_color, hover_color, command):
    b = tk.Button(
        parent,
        text=text,
        font=self.FONT_MAIN,
        bg=bg_color,
        fg="white",
        activebackground=hover_color,
        activeforeground="white",
        bd=0,
        relief="flat",
        cursor="hand2",
        padx=8,
        pady=6,
        command=command,
    )
    b.bind("<Enter>", lambda e: b.config(background=hover_color))
    b.bind("<Leave>", lambda e: b.config(background=bg_color))
    return b

  # MQTT Fonksiyonları
  def mesaj_yolla(self):
    if not self.yayın_başlığı:
      messagebox.showwarning(
          "Uyarı", "Lütfen önce geçerli bir yayın başlığı onaylayın!"
      )
      return
    mesaj = self.gönderilen_yazı_kutusu.get("1.0", tk.END).strip()
    self.client.publish(self.yayın_başlığı, "Özgür: " + mesaj)

  def mesaj_alındı(self, client, userdata, message):
    self.gelen_yazı_kutusu.insert(
        tk.END, message.payload.decode() + "\n"
    )  # Alt alta ekleme
    print(f"Mesaj alındı: {message.payload.decode()}")

  def yayın_başlığı_güncelle(self):
    self.yayın_başlığı = self.yayın_giriş.get()
    messagebox.showinfo(
        "Başlık Güncellendi", f"Yeni yayın başlığı: {self.yayın_başlığı}"
    )

  def abone_ol(self):
    topic = self.abone_giriş.get()
    if topic:
      self.client.subscribe(topic)
      messagebox.showinfo("Abonelik", f"Başarıyla abone olundu: {topic}")

  def abonelikten_çık(self):
    topic = self.abone_giriş.get()
    if topic:
      self.client.unsubscribe(topic)
      messagebox.showinfo("Abonelik", f"Abonelikten çıkıldı: {topic}")

  def bağlan(self):
    try:
      self.client.loop_stop()
      self.client.disconnect()
      broker = self.bağlantı_değişkeni.get()
      print(f"Bağlanılıyor: {broker}")
      self.client = mqtt.Client()
      self.client.on_message = self.mesaj_alındı
      self.client.on_connect = self.bağlantı_sağlandı
      self.client.connect(broker, 1883, 60)
      self.client.loop_start()
    except Exception as e:
      messagebox.showerror("Hata", f"Bağlantı kurulamadı: {e}")

  def bağlantı_sağlandı(self, client, userdata, flags, rc):
    if rc == 0:
      messagebox.showinfo(
          "Bağlantı Sağlandı", f"{client._host}:{client._port} adresine bağlanıldı."
      )
    else:
      hata_kodları = {
          1: "Connection refused: level of MQTT protocol not supported by server.",
          2: "Connection refused: client identifier not allowed by server.",
          3: "Network connection successful but MQTT service is unavailable.",
          4: "Data in username or password is malformed.",
          5: "Client not authorized to connect.",
      }
      yazı = hata_kodları.get(rc, f"Bilinmeyen hata kodu: {rc}")
      messagebox.showerror("Bağlantı Hatası", yazı)

  def _mqtt_başlat(self):
    try:
      broker = "test.mosquitto.org"
      self.client.connect(broker, 1883, 60)
      self.client.loop_start()
    except Exception as e:
      print(f"İlk bağlantı hatası: {e}")


if __name__ == "__main__":
  ekran = tk.Tk()
  app = MQTTApp(ekran)
  ekran.mainloop()