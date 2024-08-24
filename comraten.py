import random, os
import tkinter as tk
from tkinter import ttk
from tkinter import *
from tkinter.messagebox import showinfo
from collections import Counter

root = tk.Tk()
root.title('Zahlen raten')
root.geometry('600x400+50+50')

spiel = ttk.Frame(root)
spiel.pack(padx=10, pady=10, fill='x', expand=True)

ratezahl_var = tk.StringVar()
ratezahl_label = ttk.Label(spiel, text="Gib mir eine Zahl:")
ratezahl_label.pack(fill='x', expand=True)

ratezahl_entry = ttk.Entry(spiel, textvariable=ratezahl_var)
ratezahl_entry.pack(fill='x', expand=True)
ratezahl_entry.focus()
ratezahl_entry.delete(0, 'end')

arrg = []
arrk = []

# Funktionen für die Algos
def neuezahl(zahlcom):
    arrg.append(zahlcom)
    if arrk:
        untere_grenze = max(arrk)
    else:
        untere_grenze = 1
    obere_grenze = min(arrg)
    zahlcom = random.randint(untere_grenze + 1, obere_grenze - 1)
    return zahlcom

def neuezahlkleiner(zahlcom):
    arrk.append(zahlcom)
    if arrg:
        obere_grenze = min(arrg)
    else:
        obere_grenze = 100
    untere_grenze = max(arrk)
    zahlcom = random.randint(untere_grenze + 1, obere_grenze - 1)
    return zahlcom

# Welcher Button wurde geklickt und Übergabe an Funktion weiter_spiel
def which_button(t):
    global großoklein
    großoklein = t
    weiter_spiel()

def weiter_spiel():
    global großoklein, zahlcom, Zaehler
    if großoklein == "g":
        zahlcom = neuezahl(zahlcom)
    else:
        zahlcom = neuezahlkleiner(zahlcom)
    großoklein = ""
    Zaehler += 1
    result_label.config(text=f"Meine Zahl: {zahlcom}")
    ratezahl = int(ratezahl_var.get())
    if zahlcom == ratezahl:
        result3_label.config(text=f"Die Zahl ist: {zahlcom}")
        result4_label.config(text=f"Ich habe {Zaehler} Versuche gebraucht.")
        result6_label.config(text="Neues Spiel?")
        ja_button.pack(fill='x', expand=True)
        nein_button.pack(fill='x', expand=True)
        arrsintxt(arrg, arrk, ratezahl)  # Arrays in txt speichern
    else:
        result2_label.config(text="Ist meine Zahl zu groß oder zu klein?")

#Funktion start_game um alles wieder zurückzusetzen und ein leeres GUI zu haben und dann an haupt() weitergeben
def start_game():
    global zahlcom, Zaehler, arrg, arrk
    print("Starte neues Spiel...")  # Debugging 
    Zaehler = 0
    arrg.clear()
    arrk.clear()
    result_label.config(text="")
    result2_label.config(text="")
    result3_label.config(text="")
    result4_label.config(text="")
    result5_label.config(text="")
    result6_label.config(text="")
    zugross_button.pack_forget()
    zuklein_button.pack_forget()
    ja_button.pack_forget()
    nein_button.pack_forget()
    ratezahl_entry.delete(0, 'end')
    haupt()

def haupt():
    global zahlcom, Zaehler
    Zaehler = 0
    #Prüfen auf ganze Zahl
    try:
        ratezahl = int(ratezahl_var.get())
        if not (1 <= ratezahl <= 100):
            result_label.config(text="Bitte nur eine Zahl von 1 bis 100 eingeben.")
            return
    except ValueError:
        result_label.config(text="Das ist keine gültige Zahl.")
        print("ValueError: Kein gültiger Input")  # Debugging 
        return
    # Datei daten.txt einlesen und die zahl mit der höchsten wahrscheinlichkeit auslesen
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, 'daten.txt')
    numbers = []
    with open(file_path, 'r') as file:
        lines = file.readlines()
        for i in range(0, len(lines), 1):
            try:
                ratezahl = int(lines[i].strip())
                zahl = int(lines[i+1].strip())
                wahrscheinlichkeit = int(lines[i+2].strip())
                numbers.append(ratezahl)
                numbers.append(zahl)
                numbers.append(wahrscheinlichkeit)
            except (IndexError, ValueError):
                continue
    
    #Zahlen aus array numbers mithilfe von Counter einlesen zählen und nur die wahrscheinlichste Zahl in zahlcom speichern
    #!!!Problem noch: Wenn eine Zahl oft vorkommt wird keine andere mehr genommen. 
    if numbers:
        counter = Counter(numbers)
        most_probable_number = counter.most_common(1)[0][0]
        zahlcom = most_probable_number  # nimm die häufigste Zahl als zahlcom
    else:
        result_label.config(text="Keine Zahlen gefunden.")
        zahlcom = random.randint(1, 100)  # Wenn keine Zahl gefunden, nimm von 1 bis 100

    result_label.config(text=f"Meine Ratezahl: {zahlcom}")
    result2_label.config(text="Ist meine Zahl zu groß oder zu klein?")
    zugross_button.pack(fill='x', expand=True)
    zuklein_button.pack(fill='x', expand=True)

#Funktion um die Daten aus den arrays und der Variable in daten.txt zu speichern
def arrsintxt(arrg, arrk, ratezahl):
    # Wo liegt das programm
    script_dir = os.path.dirname(os.path.abspath(__file__))
    # abspeichern des absoluten pfades in datei
    datei = os.path.join(script_dir, 'daten.txt')
    with open(datei, 'a') as file:
        file.write(f'{ratezahl}\n')
        #!!!Problem: Ratezahl wird trotz neustarts erneut geschrieben. und nicht alles wird geschrieben
        for zahl, wahrscheinlichkeit in zip(arrg, arrk):
            file.write(f'{zahl}\n{wahrscheinlichkeit}\n')

inputcheck_button = ttk.Button(spiel, text="Abschicken", command=haupt)
inputcheck_button.pack(fill='x', expand=True)

result_label = ttk.Label(spiel)
result_label.pack(fill='x', expand=True)
result2_label = ttk.Label(spiel)
result2_label.pack(fill='x', expand=True)
result3_label = ttk.Label(spiel)
result3_label.pack(fill='x', expand=True)
result4_label = ttk.Label(spiel)
result4_label.pack(fill='x', expand=True)
result5_label = ttk.Label(spiel)
result5_label.pack(fill='x', expand=True)
result6_label = ttk.Label(spiel)
result6_label.pack(fill='x', expand=True)

zugross_button = ttk.Button(spiel, text="Ist zu Groß", command=lambda: which_button("g"))
zuklein_button = ttk.Button(spiel, text="Ist zu klein", command=lambda: which_button("k"))
ja_button = ttk.Button(spiel, text="Ja", command=start_game)
nein_button = ttk.Button(spiel, text="Nein", command=root.quit)

root.mainloop()