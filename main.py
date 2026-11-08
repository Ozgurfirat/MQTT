
"""
Bu proje github üzerinden paylaşılmaktadır

"""

"""
MQTT
Hafiftir: Küçük paket boyutları sayesinde internet kotasını ve işlemci gücünü yormaz.
Enerji Tasarrufu Sağlar: Pilli ve uzaktaki cihazların uzun süre çalışmasına yardım eder.
Hızlıdır: Anlık veri paylaşımı sunar.

"""

from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import paho.mqtt.client as mqtt

global client
global yayın_başlığı
global mesaj_alındı

def mesaj_yolla():
    global yayın_başlığı
    global client
    # burada yorum var githubda görünen
    mesaj = gönderilen_yazı_kutusu.get("1.0",END)
    client.publish(yayın_başlığı, "Özgür: " + mesaj)

# parantez içinde yer alan parametreler yazılmalıdır
def mesaj_alındı(client, userdata, message):
    gelen_yazı_kutusu.insert(END , message.payload.decode())
    print("Krşıdan mesaj alındı (GITHUB deneme)")
    print(f"Mesaj alındı: {message.payload.decode()}")


def yayın_başlığı_güncelle():
    global yayın_başlığı
    yayın_başlığı = yayın_giriş.get()

def abone_ol():
    global client
    client.subscribe(abone_giriş.get())

def bağlan():
    global yayın_başlığı
    global client
    client.loop_stop()# bir önceki client döngüsünü durdur
    client.disconnect() # bağlantıyı kapat
    print(bağlantı_değişkeni.get())
    client.on_message = mesaj_alındı
    client.on_connect = bağlantı_sağlandı
    client.connect(bağlantı_değişkeni.get(), 1883, 60)
    client.loop_start() # yeni client için döngüyü başlat

def bağlantı_sağlandı(client, userdata, flags, rc):# içindeki parametreler yazılmalı yoksa hata verir
    if rc == 0: # iletişim tamam haberleşme yapılablir.
        messagebox.showinfo("Bağlantı Sağlandı" , f"{client._host}:{client._port} bağlanıldı")
    else:
        print("bağlantı hatası:" , rc)
        if rc == 1:
            yazı = "Connection refused: level of MQTT protocol not supported by server."
        elif rc == 2:
            yazı = "Connection refused: client identifier not allowed by server."
        elif rc == 3:
            yazı = "Network connection successful but MQTT service is unavailable."
        elif rc == 4:
            yazı = "Data in username or password is malformed."# kullanıcı adı veya parola yanlış !!
        elif rc == 5:
            yazı = "Client not authorized to connect."
        messagebox.showerror("Bağlantı Hatası" , yazı)

if __name__ == '__main__':
    ekran = Tk()
    bağlantı_değişkeni = StringVar()
    abone_değişkeni = StringVar()

    # MQTT için gerekli kodlar yazılıyor
    broker = "test.mosquitto.org"  # Örnek bir broker
    port = 1883 # genel amaçlı test için şifresiz port

    yayın_başlığı = bağlantı_değişkeni.get()

    client = mqtt.Client()

    client.on_message = mesaj_alındı # karşıdan mesaj alındığında çalışacak olan fonksiyon tanımlanıyor
    client.on_connect = bağlantı_sağlandı

    client.connect(broker, port, 60)


    # ______________ G U I tasarımı ____________________________
    yazı_fontu = ("Arial 17 bold")
    gelen_etiketi = Label(ekran , font = yazı_fontu , text = "GELEN VERİ")
    gelen_etiketi.grid (row =0 , column = 0 , padx= 10 ,pady= 10)
    gelen_yazı_kutusu = Text(ekran , font = yazı_fontu , width = 30 , height = 13)
    gelen_yazı_kutusu.grid(row= 1 , column = 0 , padx = 10 , pady = 10 , rowspan = 2)

    gönderilen_etiketi = Label(ekran , font = yazı_fontu , text = "GÖNDERİLEN VERİ")
    gönderilen_etiketi.grid (row =0 , column = 1 , padx= 10 ,pady= 10)
    gönderilen_yazı_kutusu = Text(ekran , font = yazı_fontu , width = 30 , height = 13)
    gönderilen_yazı_kutusu.grid(row= 1 , column = 1 , padx = 10 , pady = 10 , rowspan = 2)

    abone_yazısı = Label(ekran , font = yazı_fontu , text = "ABONE BAŞLIĞI")
    abone_yazısı.grid(row= 2 , column = 0 , padx = 10 , pady = 10 )
    yayınlama_yazısı = Label(ekran , font = yazı_fontu , text = "YAYINLAMA BAŞLIĞI")
    yayınlama_yazısı.grid(row= 2 , column = 1 , padx = 10 , pady = 10 )

    abone_giriş = Entry(ekran, font = yazı_fontu )
    abone_giriş.grid(row = 3 , column = 0 , padx = 10 , pady = 10 )
    yayın_giriş = Entry(ekran, font = yazı_fontu )
    yayın_giriş.grid(row = 3 , column = 1 , padx = 10 , pady = 10 )
    abone_onay_tuşu = Button(ekran , font = yazı_fontu , text = "Abone Ol" , command = abone_ol)
    abone_onay_tuşu.grid(row = 4 , column = 0 , padx = 10 , pady = 10 )
    yayın_onay_tuşu = Button(ekran , font = yazı_fontu , text = "Yayın Onayla" , command = yayın_başlığı_güncelle)
    yayın_onay_tuşu.grid(row = 4 , column = 1 , padx = 10 , pady = 10 )

    # bağlantı işlemleri çerçevesi
    bağlantı_çerçevesi = Frame (ekran ,bd = 3 , relief=GROOVE)
    bağlantı_çerçevesi.grid(row = 1  ,column = 2 , padx = 10 , pady = 10 , sticky=N)
    bağlantı_yazısı = Label(bağlantı_çerçevesi , text = "BAĞLANTI İŞLEMLERİ" , font = yazı_fontu)
    bağlantı_yazısı.grid(row = 0 , column = 0 , padx = 10 , pady = 10 )
    bağlantı_adresleri = ["test.mosquitto.org" , "broker.hivemq.com" , "broker.emqx.io"]
    bağlantı_combobox = ttk.Combobox(bağlantı_çerçevesi , textvariable= bağlantı_değişkeni , width = 30 ,
                                     font = yazı_fontu )
    bağlantı_combobox.grid(row = 1 , column = 0 , padx = 10 , pady = 10)
    bağlantı_combobox['values'] = bağlantı_adresleri
    bağlan_tuşu = Button(bağlantı_çerçevesi , text= "BAĞLAN" , font = yazı_fontu , command = bağlan)
    bağlan_tuşu.grid(row = 2 , column = 0 , padx = 10 , pady = 10 )
    mesaj_gönder_tuşu = Button(ekran , font = yazı_fontu , text = "MESAJ\nGÖNDER" , command = mesaj_yolla)
    mesaj_gönder_tuşu.grid(row = 3 , column =2 ,padx = 10 , pady = 10 )

    # abonelik çerçevesi ve işlemleri
    abone_çerçevesi = Frame(ekran , bd = 3 , relief=GROOVE)
    abone_çerçevesi.grid(row = 2 , column = 2 , padx = 10 , pady = 10)
    abonelik_yazısı = Label(abone_çerçevesi, text="ABONELİK İŞLEMLERİ", font=yazı_fontu)
    abonelik_yazısı.grid(row=0, column=0, padx=10, pady=10 , columnspan = 2)

    abone_combobox = ttk.Combobox(abone_çerçevesi, textvariable=abone_değişkeni, width=30,
                   font=yazı_fontu)
    abone_combobox.grid(row=1, column=0, padx=10, pady=10, columnspan = 2)
    abone_combobox['values'] = []

    abone_ol_tuşu = Button(abone_çerçevesi, text="Abone\nOl", font=yazı_fontu, command=abone_ol)
    abone_ol_tuşu.grid(row=2, column=0, padx=10, pady=10)
    abonelikten_çık_tuşu = Button(abone_çerçevesi, text="Abonelikten\nÇık", font=yazı_fontu, command=abone_ol)
    abonelikten_çık_tuşu.grid(row=2, column=1, padx=10, pady=10)

    #   ---------------- D İ K K  A T   _________________________
    client.loop_start() # önce mqtt loop_start yazılır

    ekran.mainloop() # en son ekran.mainloop() yazılır







