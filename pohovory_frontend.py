from tkinter import *
import sqlite3


"""
Jak maji tlacitka pracovat:
dHledat:
    - Pokud v DB existuje zaznam se shodujicim se jmenem spolecnosti nebo tel. cisla
    - Vypise jej
dUlozit jako nove:
    - Ulozi vstup jako novy pohovor, pokud je vyplnena alespon spolecnost nebo tlf
dUlozit zmeny:
    - Ulozi zmeny v nactenem pohovoru
dVypis vse:
    - Do pozn8mky vypise Spolecnost, pohovor (dle ulozeni v db)
dVypis dle data:
    - Do pozn8mky vypise Spolecnost, pohovor (dle nejblizsiho data)
dVycisti:
    - Vycisti vstupni pole
dVymaz oznacene:
    - Vymaze oznaceny radek z DB
dVypnout:
    - Vypinaci tlacitko
TODO:
-pokud budes mit volno (ach, kez by :-)) predelej vypis dle data tak, aby to bralo a pocitalo jen s realnym datumem
- predej to na dva fily - back+front end... bude to srani, ale ano, udelej to
"""
"""
BACKEND
"""

def smaz_oznacene():
    id_k_smazani = selected_row
    spojeni = sqlite3.connect('pohovory.db')
    kurzor = spojeni.cursor()
    kurzor.execute("DELETE FROM pohovory WHERE id = ?", str(id_k_smazani))
    spojeni.commit()
    spojeni.close()
    vloz_do_t1('Smazan pohovor s id: {}'.format(id_k_smazani), prepis = True)

def get_selected_row(event):
    global selected_row
    index = list1_vypis_polozek.curselection()[0]
    selected_row = list1_vypis_polozek.get(index)[0]#[0]
    vypsat_oznacene_do_poli()

def vycisti_pole():
    for pole in seznam_vstupnich_poli[:-1]:
        pole.delete(0, END)
    seznam_vstupnich_poli[-1].delete(1.0, END)

def spojeni_s_db():
    spojeni = sqlite3.connect('pohovory.db')
    kurzor = spojeni.cursor()
    kurzor.execute("CREATE TABLE IF NOT EXISTS pohovory(id INTEGER PRIMARY KEY, firma text, pohovor text, osoba1 text, osoba2 text, osoba3 text, mail1 text, mail2 text, mail3 text, telefon1 text, telefon2 text, telefon3 text, poznamka1 text, poznamka2 text, poznamka3 text, poznamky text)")
    spojeni.commit()
    spojeni.close()

def vypsat_oznacene_do_poli():
    id_k_vypsani = selected_row
    spojeni = sqlite3.connect('pohovory.db')
    kurzor = spojeni.cursor()
    kurzor.execute("SELECT * FROM pohovory WHERE id = ?", str(id_k_vypsani))
    seznam_k_vypsani = kurzor.fetchall()
    vycisti_pole()
    for i, obj in enumerate(seznam_k_vypsani[0][1:]):
        seznam_vstupnich_poli[i].insert(END, obj)
    spojeni.close()

def vlozeni_noveho_zaznamu():
    if len(e1_firma_value.get()) == len(e9_number1_value.get()) ==  len(e2_pohovor_value.get()) == 0:
        vloz_do_t1('Neni co ukladat... co takhle se více snažit?')
        return
    spojeni = sqlite3.connect('pohovory.db')
    kurzor = spojeni.cursor()
    kurzor.execute("INSERT INTO pohovory VALUES(NULL, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (e1_firma_value.get(), e2_pohovor_value.get(), e3_osoba1_value.get(), e4_osoba2_value.get(), e5_osoba3_value.get(), e6_mail1_value.get(), e7_mail2_value.get(), e8_mail3_value.get(), e9_number1_value.get(), e10_number2_value.get(), e11_number3_value.get(), e12_popisek1_value.get(), e13_popisek2_value.get(), e14_popisek3_value.get(), t1_poznamky.get("1.0", 'end-1c')))
    spojeni.commit()
    spojeni.close()
    vloz_do_t1('Zaznam uspesne pridan :-)', True)

def vloz_do_t1(objekt, prepis = True):
    # Funkce, ktera do Poznamkoveho pole vklada hodnoty. Pokud prepis = True:smaze puvodni vypsany obsah pole
    if prepis:
        list1_vypis_polozek.delete(0, END)
    list1_vypis_polozek.insert(END, objekt)

def nacti_vse_dle_abecedy():
    spojeni = sqlite3.connect('pohovory.db')
    kurzor = spojeni.cursor()
    kurzor.execute("SELECT id, firma, pohovor FROM pohovory ORDER BY firma ASC")
    vytah_z_db = kurzor.fetchall()
    # vycisti_pole()
    list1_vypis_polozek.delete(0, END)
    for objekt in vytah_z_db:
        vloz_do_t1(objekt, prepis = False)
    spojeni.close()

def nacti_vse_dle_data():
    spojeni = sqlite3.connect('pohovory.db')
    kurzor = spojeni.cursor()
    kurzor.execute("SELECT id, firma, pohovor FROM pohovory ORDER BY pohovor ASC")
    vytah_z_db = kurzor.fetchall()
    list1_vypis_polozek.delete(0, END)
    for objekt in vytah_z_db:
        vloz_do_t1(objekt, prepis = False)
    spojeni.close()

def hledat():
    if len(e1_firma_value.get()) == len(e9_number1_value.get()) ==  len(e2_pohovor_value.get()) == 0:
        vloz_do_t1('Není dle čeho hledat. Víc se snaž')
        return
    spojeni = sqlite3.connect('pohovory.db')
    kurzor = spojeni.cursor()
    kurzor.execute(
        "SELECT id, firma, pohovor FROM pohovory WHERE telefon1 = ? OR telefon2 = ? OR telefon3 = ?",
        (e9_number1_value.get(), e9_number1_value.get(),
         e9_number1_value.get()))
    vysledek = kurzor.fetchall()[0]
    vloz_do_t1(vysledek, prepis = True)
    spojeni.close()

def update_zapisu():
    spojeni = sqlite3.connect('pohovory.db')
    kurzor = spojeni.cursor()
    kurzor.execute("UPDATE pohovory SET firma = ?, pohovor = ?, osoba1 = ?, osoba2 = ?, osoba3 = ?, mail1 = ?, mail2 = ?, mail3 = ?, telefon1 = ?, telefon2 = ?, telefon3 = ?, poznamka1 = ?, poznamka2 = ?, poznamka3 = ?, poznamky = ? WHERE firma = ?", (e1_firma_value.get(), e2_pohovor_value.get(), e3_osoba1_value.get(), e4_osoba2_value.get(), e5_osoba3_value.get(), e6_mail1_value.get(), e7_mail2_value.get(), e8_mail3_value.get(), e9_number1_value.get(), e10_number2_value.get(), e11_number3_value.get(), e12_popisek1_value.get(), e13_popisek2_value.get(), e14_popisek3_value.get(), t1_poznamky.get("1.0", 'end-1c'), e1_firma_value.get()))
    spojeni.commit()
    spojeni.close()

def vypnout():
    window.destroy()

spojeni_s_db()
"""
FRONTEND
"""


window = Tk()
window.wm_title('Pohovory v0.2')

l1_firma = Label(window, text = 'Společnost:')
l1_firma.grid(row = 0, column = 0, sticky = W+S)
e1_firma_value = StringVar()
e1_firma = Entry(window, textvariable = e1_firma_value)
e1_firma.grid(row = 1, column = 0, sticky = W+S+N)
e1_firma.config(font=("Times", 12, 'bold'))

l2_pohovor = Label(window, text = '      Pohovor:')
l2_pohovor.grid(row = 1, column = 1, columnspan = 2, sticky = W+S)
e2_pohovor_value = StringVar()
e2_pohovor = Entry(window, textvariable = e2_pohovor_value)
e2_pohovor.grid(row = 1, column = 1, columnspan = 2, sticky = S)

l3_osoba1 = Label(window, text = 'Osoba1:')
l3_osoba1.grid(row = 2, column = 0, sticky = S+W)
e3_osoba1_value = StringVar()
e3_osoba1 = Entry(window, textvariable = e3_osoba1_value)
e3_osoba1.grid(row = 3, column = 0, sticky = W)

l4_osoba2 = Label(window, text = 'Osoba2:')
l4_osoba2.grid(row = 2, column = 1, sticky = W+S)
e4_osoba2_value = StringVar()
e4_osoba2 = Entry(window, textvariable = e4_osoba2_value)
e4_osoba2.grid(row = 3, column = 1, sticky = W)

l5_osoba3 = Label(window, text = 'Osoba3:')
l5_osoba3.grid(row = 2, column = 2, sticky = S+W)
e5_osoba3_value = StringVar()
e5_osoba3 = Entry(window, textvariable = e5_osoba3_value)
e5_osoba3.grid(row = 3, column = 2, sticky = W)

l6_mail1 = Label(window, text = 'E-mail:')
l6_mail1.grid(row = 4, column = 0, sticky = S+W)
e6_mail1_value = StringVar()
e6_mail1 = Entry(window, textvariable = e6_mail1_value)
e6_mail1.grid(row = 5, column = 0, sticky = W)

e7_mail2_value = StringVar()
e7_mail2 = Entry(window, textvariable = e7_mail2_value)
e7_mail2.grid(row = 5, column = 1, sticky = W)

e8_mail3_value = StringVar()
e8_mail3 = Entry(window, textvariable = e8_mail3_value)
e8_mail3.grid(row = 5, column = 2, sticky = W)

l7_telefon1 = Label(window, text = 'Telefonní číslo:')
l7_telefon1.grid(row = 6, column = 0, sticky = S+W)
e9_number1_value = StringVar()
e9_number1 = Entry(window, textvariable = e9_number1_value)
e9_number1.grid(row = 7, column = 0, sticky = W)
e10_number2_value = StringVar()
e10_number2 = Entry(window, textvariable = e10_number2_value)
e10_number2.grid(row = 7, column = 1, sticky = W)
e11_number3_value = StringVar()
e11_number3 = Entry(window, textvariable = e11_number3_value)
e11_number3.grid(row = 7, column = 2, sticky = W)

l8_popisek1 = Label(window, text = 'Pozn.:')
l8_popisek1.grid(row = 8, column = 0, sticky = S+W)
e12_popisek1_value = StringVar()
e12_popisek1 = Entry(window, textvariable = e12_popisek1_value)
e12_popisek1.grid(row = 9, column = 0, sticky = W)
e13_popisek2_value = StringVar()
e13_popisek2 = Entry(window, textvariable = e13_popisek2_value)
e13_popisek2.grid(row = 9, column = 1, sticky = W)
e14_popisek3_value = StringVar()
e14_popisek3 = Entry(window, textvariable = e14_popisek3_value)
e14_popisek3.grid(row = 9, column = 2, sticky = W)

list1_vypis_polozek = Listbox(window, height = 14, width = 44)
list1_vypis_polozek.grid(row = 10, column = 0, rowspan = 14, columnspan = 2, sticky = W+N)

s1 = Scrollbar(window)
s1.grid(row = 18, column = 2, rowspan = 15, sticky = E+N+S)
list1_vypis_polozek.bind('<<ListboxSelect>>', get_selected_row)

t1_poznamky = Text(window, height = 15, width = 70)
t1_poznamky.configure(yscrollcommand = s1.set)
t1_poznamky.grid(row = 18, column = 0, columnspan = 3, sticky = W)
s1.configure(command = t1_poznamky.yview)

seznam_vstupnich_poli = [e1_firma, e2_pohovor, e3_osoba1, e4_osoba2, e5_osoba3, e6_mail1, e7_mail2, e8_mail3, e9_number1, e10_number2, e11_number3, e12_popisek1, e13_popisek2, e14_popisek3, t1_poznamky]


### Tlacitka


b1_find = Button(window, text = 'Hledat')
b1_find.config(height = 0, command = hledat)
b1_find.grid(row = 10, column = 2, sticky = W+E)
b2_save_new = Button(window, text = 'Uložit jako nové', command = vlozeni_noveho_zaznamu)
b2_save_new.grid(row = 11, column = 2, sticky = W+E)
b3_save_changes = Button(window, text = 'Uložit změny', command = update_zapisu)
b3_save_changes.grid(row = 12, column = 2, sticky = W+E)
b4_print_all = Button(window, text = 'Vypiš vše dle abecedy', command = nacti_vse_dle_abecedy)
b4_print_all.grid(row = 13, column = 2, sticky = W+E)
b5_sort_time = Button(window, text = 'Vypiš vše dle data', command = nacti_vse_dle_data)
b5_sort_time.grid(row = 14, column = 2, sticky = W+E)
b6_clear = Button(window, text = 'Vyčisti pole', command = vycisti_pole)
b6_clear.grid(row = 15, column = 2, sticky = W+E)
b7_delete_selected = Button(window, text ='Vymazat označené', command = smaz_oznacene)
b7_delete_selected.grid(row = 16, column = 2, sticky = W + E)
b8_exit = Button(window, text = 'Vypnout', command = vypnout)
b8_exit.grid(row = 17, column = 2, sticky = W+E)

window.mainloop()
