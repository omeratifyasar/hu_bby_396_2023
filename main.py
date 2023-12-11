from tkinter import *
from tkinter import ttk
import sqlite3
from tkinter import messagebox


pencere = Tk()
pencere.title('Katalog: Eserleri Listele')
pencere.geometry('700x470')
pencere.resizable = True
pencere['bg'] = "#0000FF"

eserTabloCercevesi = ttk.Frame(pencere, padding=25)
eserTabloCercevesi.pack()

eserTablosu = ttk.Treeview(eserTabloCercevesi)

eserTablosu['columns'] = ('id', 'price', 'title', 'author', 'genre', 'rating')

eserTablosu.column("#0", width=0, stretch=NO)
eserTablosu.column("id", anchor=CENTER, width=50)
eserTablosu.column("price", anchor=CENTER, width=25)
eserTablosu.column("title", anchor=CENTER, width=150)
eserTablosu.column("author", anchor=CENTER, width=150)
eserTablosu.column("genre", anchor=CENTER, width=125)
eserTablosu.column("rating", anchor=CENTER, width=100)

eserTablosu.heading("#0", text="", anchor=CENTER)
eserTablosu.heading("id", text="ID", anchor=CENTER)
eserTablosu.heading("price", text="Fiyat", anchor=CENTER)
eserTablosu.heading("title", text="Başlık", anchor=CENTER)
eserTablosu.heading("author", text="Yazar", anchor=CENTER)
eserTablosu.heading("genre", text="Kategori", anchor=CENTER)
eserTablosu.heading("rating", text="Değerlendirme", anchor=CENTER)

eserTablosu.pack()

baglanti = sqlite3.connect("omeratifyasar.db")
sorgu = baglanti.cursor()
sonuc = sorgu.execute("SELECT * FROM Eser")

for index, eser in enumerate(sonuc.fetchall()):
    eserTablosu.insert(parent='', index='end', iid=index, text='',
                       values=(eser[0], eser[5], eser[1], eser[2], eser[3], eser[6]))

def aramaYap():
    anahtar = arama.get()
    aramaSonuc = sorgu.execute(
        "SELECT * FROM Eser WHERE title LIKE('%{}%') OR author LIKE('%{}%') OR genre LIKE('%{}%') ORDER BY title DESC".format(
            anahtar, anahtar, anahtar)
    )

    for row in eserTablosu.get_children():
        eserTablosu.delete(row)

    for index, eser in enumerate(aramaSonuc.fetchall()):
        eserTablosu.insert(parent='', index='end', iid=index, text='',
                           values=(eser[0], eser[5], eser[1], eser[2], eser[3], eser[6]))

def eseriSil():
    selected_item = eserTablosu.selection()
    if selected_item:
        eser_id = eserTablosu.item(selected_item)['values'][0]
        sorgu.execute("DELETE FROM books WHERE id=?", (eser_id,))
        baglanti.commit()
        messagebox.showinfo("Başarı", "Eser silindi.")
        aramaYap()
        sorgu.execute("DELETE FROM books WHERE id=?", (eser_id,))
    else:
        messagebox.showerror("Hata", "Lütfen bir eser seçin.")

def eseriGuncelle():
    selected_item = eserTablosu.selection()
    if selected_item:
        eser_id = eserTablosu.item(selected_item)['values'][0]

        messagebox.showinfo("Başarı", "Eser güncellendi.")
        aramaYap()
    else:
        messagebox.showerror("Hata", "Lütfen bir eser seçin.")


aramaBaslik = Label(eserTabloCercevesi, text="Arama:")
arama = Entry(eserTabloCercevesi, width=25)
ara = Button(eserTabloCercevesi, text="Arama Yap!", command=aramaYap)
silButton = Button(eserTabloCercevesi, text="Seçilen Eseri Sil", command=eseriSil)
guncelleButton = Button(eserTabloCercevesi, text="Seçilen Eseri Güncelle", command=eseriGuncelle)

aramaBaslik.pack()
arama.pack()
ara.pack()
silButton.pack()
guncelleButton.pack()

pencere.mainloop()

