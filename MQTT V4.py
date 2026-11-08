import threading
import tkinter as tk
from tkinter import messagebox, scrolledtext
from cryptography.fernet import Fernet
import paho.mqtt.client as mqtt


# --- YAPILANDIRMA ---
# Güvenlik için aynı anahtarı iki tarafın da bilmesi gerekir.
# Gerçek projede bunu güvenli bir şekilde paylaşmalısınız.
# Test için sabit bir anahtar kullanıyoruz:
SECRET_KEY = b'1234567890abcdef1234567890abcdef1234567890I='
try:
    cipher = Fernet(SECRET_KEY)
except Exception:
    # Eğer anahtar formata uymuyorsa geçici yeni üretir (test amaçlı)
    SECRET_KEY = Fernet.generate_key()
    cipher = Fernet(SECRET_KEY)

BROKER = "test.mosquitto.org"
PORT = 1883
TOPIC = "python/tkinter/Özgür"
ABONE_BAŞLIĞI = "python/tkinter/Ayaz"


class MqttChatApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Python & MQTT Güvenli Sohbet")
        self.root.geometry("550x800")

        # Arayüz Bileşenleri
        self.create_widgets()

        # MQTT İstemci Kurulumu
        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message

        # MQTT'yi arka planda (thread içinde) başlat
        self.start_mqtt()

    def create_widgets(label):
        pass  # Fonksiyon içinde dolduruluyor

    def create_widgets(self):
        # Sohbet Geçmişi Ekranı
        self.chat_area = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, state='disabled', font=("Arial", 17))
        self.chat_area.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        # Mesaj Giriş Alanı
        self.msg_entry = tk.Entry(self.root, font=("Arial", 23))
        self.msg_entry.pack(padx=10, pady=5, fill=tk.X)
        self.msg_entry.bind("<Return>", lambda event: self.send_message())

        # Gönder Butonu
        self.send_btn = tk.Button(self.root, text="Gönder", bg="#4CAF50", fg="white", font=("Arial", 10, "bold"),
                                  command=self.send_message)
        self.send_btn.pack(padx=10, pady=5, fill=tk.X)

        # Durum Çubuğu
        self.status_label = tk.Label(self.root, text="Durum: Bağlanıyor...", fg="orange", font=("Arial", 9))
        self.status_label.pack(pady=5)

    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            self.status_label.config(text="Durum: Bağlandı & Güvenli", fg="green")
            self.client.subscribe(ABONE_BAŞLIĞI)
        else:
            self.status_label.config(text=f"Bağlantı Hatası (Kod: {rc})", fg="red")

    def on_message(self, client, userdata, msg):
        try:
            # Şifreli veriyi çöz
            decrypted_msg = cipher.decrypt(msg.payload).decode('utf-8')
            self.display_message(f"Karşı Taraf: {decrypted_msg}")
        except Exception as e:
            # Şifre uyuşmazlığı veya bozuk paket durumu
            self.display_message("[Sistem]: Şifre çözülemedi (Yetkisiz mesaj)")

    def display_message(self, message):
        # Tkinter arayüzünü ana thread dışında güvenli güncellemek için
        self.chat_area.config(state='normal')
        self.chat_area.insert(tk.END, message + "\n")
        self.chat_area.config(state='disabled')
        self.chat_area.see(tk.END)

    def send_message(self):
        message = self.msg_entry.get().strip()
        if message:
            try:
                # Mesajı şifrele
                encrypted_msg = cipher.encrypt(message.encode('utf-8'))
                # MQTT ile yayınla
                self.client.publish(TOPIC, encrypted_msg)

                self.display_message(f"Ben: {message}")
                self.msg_entry.delete(0, tk.END)
            except Exception as e:
                messagebox.showerror("Hata", f"Mesaj gönderilemedi: {e}")

    def start_mqtt(self):
        def run():
            try:
                self.client.connect(BROKER, PORT, 60)
                self.client.loop_forever()
            except Exception as e:
                self.status_label.config(text="Broker bağlantısı kurulamadı!", fg="red")

        t = threading.Thread(target=run, daemon=True)
        t.start()


if __name__ == "__main__":
    root = tk.Tk()
    app = MqttChatApp(root)
    root.mainloop()