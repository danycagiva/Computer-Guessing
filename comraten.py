import random, os
import tkinter as tk
from tkinter import ttk
from tkinter import *
from tkinter.messagebox import showinfo
from collections import Counter
import numpy as np

root = tk.Tk()
root.title('Zahlen raten')
root.geometry('600x400+50+50')

spiel = ttk.Frame(root)
spiel.pack(padx=10, pady=10, fill='x', expand=True)


def tippse(label, text, delay=100):
    if text:
        current_text = label.cget("text")
        label.config(text=current_text + text[0])
        label.after(delay, tippse, label, text[1:], delay)

ratezahl_var = tk.StringVar()
ratezahl_label = ttk.Label(spiel, text="")
ratezahl_label.pack(fill='x', expand=True)
tippse(ratezahl_label, "Gib mir eine Zahl", 100)
ratezahl_entry = ttk.Entry(spiel, textvariable=ratezahl_var)
ratezahl_entry.pack(fill='x', expand=True)
ratezahl_entry.focus()
ratezahl_entry.delete(0, 'end')

arrg = []
arrk = []

# Funktionen für die Algos
def neuezahl(zahlcom):
    global filtered
    arrg.append(zahlcom)
    if arrk:
        untere_grenze = max(arrk)
    else:
        untere_grenze = 0
    obere_grenze = min(arrg)


    #strip alle zahlen die größer sind als min(arrg) aus dem dataset
    filtered = filter(lambda num: num < min(arrg), filtered)
    filtered=list(filtered)
    print(filtered)#Debugging Line
    # Dataset in zahlwerte laden
    zahl_werte = filtered  
    mittel_wert = (np.max(zahl_werte) + np.min(zahl_werte)) / 2  # Mittlerer Wert der Zahlen der auch in die csv muss
    variabilität = np.std(zahl_werte)  # Variabilität der Zahlen - muss auch in csv

    X = np.array([[mittel_wert, variabilität] for _ in range(len(filtered))])  # Matrix von Eigenschaften
    y = zahl_werte  # Vektor von Zahlen

    # Lade das Dataset und trainiere ein k-NN-Modell
    from sklearn.neighbors import KNeighborsRegressor
    knn = KNeighborsRegressor(n_neighbors=5)#erzeugen mit 5 nachbarn
    knn.fit(X, y)

    def vorhersage(eigenschaften):
            return knn.predict(np.array([eigenschaften]))

    # Eigenschaften der Zahl
    eigenschaften = [mittel_wert, variabilität]  # Mittlerer Wert und Variabilität
    vorhersagte_zahl = vorhersage(eigenschaften)
    zahlcom=int(vorhersagte_zahl[0])
    print(vorhersagte_zahl) #Debug-Line


    #zahlcom = random.randint(untere_grenze + 1, obere_grenze - 1)
    return zahlcom
    #abfangen Wenn range zahl1-1=zahl1 return valueerror and generate new range between array-1 and array+1

def neuezahlkleiner(zahlcom):
    global filtered
    arrk.append(zahlcom)
    #strip alle zahlen die kleiner sind alle max(arrk) aus dem dataset

    if arrg:
        obere_grenze = min(arrg)
    #elif max(arrg) > max(arrk-1):
    #    obere_grenze = 101  
    else:
        obere_grenze = 101


    untere_grenze = max(arrk)
    filtered = filter(lambda num: num > max(arrk), filtered)
    filtered=list(filtered)
    print(filtered)
    # Dataset in zahlwerte laden
    zahl_werte = filtered  
    mittel_wert = (np.max(zahl_werte) + np.min(zahl_werte)) / 2  # Mittlerer Wert der Zahlen der auch in die csv muss
    variabilität = np.std(zahl_werte)  # Variabilität der Zahlen - muss auch in csv

    X = np.array([[mittel_wert, variabilität] for _ in range(len(filtered))])  # Matrix von Eigenschaften
    y = zahl_werte  # Vektor von Zahlen

    # Lade das Dataset und trainiere ein k-NN-Modell
    from sklearn.neighbors import KNeighborsRegressor
    knn = KNeighborsRegressor(n_neighbors=5)#erzeugen mit 5 nachbarn
    knn.fit(X, y)

    def vorhersage(eigenschaften):
            return knn.predict(np.array([eigenschaften]))

    # Eigenschaften der Zahl
    eigenschaften = [mittel_wert, variabilität]  # Mittlerer Wert und Variabilität
    vorhersagte_zahl = vorhersage(eigenschaften)
    zahlcom=int(vorhersagte_zahl[0])
    print(vorhersagte_zahl) #Debug-Line
    #zahlcom = random.randint(untere_grenze + 1, obere_grenze - 1)
    return zahlcom
    #abfangen Wenn range zahl1-1=zahl2+2 return valueerror and generate new range between array-1 and array+1


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
    result_label.config(text="")
    tippse(result_label, f"Meine Zahl: {zahlcom}", 100)
    #result_label.config(text=f"Meine Zahl: {zahlcom}")
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
    ratezahl_entry.delete(0)
    haupt()

def haupt():
    global zahlcom, Zaehler, filtered
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
    result_label.config(text="")
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
                #print(numbers)
            except (IndexError, ValueError):
                continue
    filtered=numbers
    #Zahlen aus array numbers mithilfe von Counter einlesen zählen und nur die wahrscheinlichste Zahl in zahlcom speichern
    if numbers:
        #counter = Counter(numbers)
        #get 10 numbers and count probability with most.common out of array numbers and return new number
        #most_probable_number = counter.most_common(10)
        #print(most_probable_number) #Debugging Line
        #zahlcom2 = random.choice(most_probable_number)  # nimm die häufigste array-Zahl als zahlcom2
        #zahlcom = zahlcom2[0] #nimm position0 als neue Zahl
        
        # Dataset in zahlwerte laden
        zahl_werte = numbers  
        mittel_wert = (np.max(zahl_werte) + np.min(zahl_werte)) / 2 #(np.max(zahl_werte) + np.min(zahl_werte)) / 2  # Mittlerer Wert der Zahlen der auch in die csv muss
        variabilität = np.std(zahl_werte)  # Variabilität der Zahlen - muss auch in csv

        X = np.array([[mittel_wert, variabilität] for _ in range(len(zahl_werte))])  # Matrix von Eigenschaften
        y = zahl_werte  # Vektor von Zahlen

        # Lade das Dataset und trainiere ein k-NN-Modell
        from sklearn.neighbors import KNeighborsRegressor
        knn = KNeighborsRegressor(n_neighbors=10)#erzeugen mit 5 nachbarn
        knn.fit(X, y)

        def vorhersage(eigenschaften):
            return knn.predict(np.array([eigenschaften]))

        # Eigenschaften der Zahl
        eigenschaften = [mittel_wert, variabilität]  # Mittlerer Wert und Variabilität
        vorhersagte_zahl = vorhersage(eigenschaften)
        zahlcom=int(vorhersagte_zahl[0])
        print(vorhersagte_zahl) #Debug-Line
    else:
        result_label.config(text="Keine Zahlen gefunden.")
        # Erstelle das Dataset von 1-100 wenn nichts funktioniert//als fallback
        zahl_werte = np.random.randint(1, 100, size=(1000))  # 1000 Zahlen zwischen 1 und 100
        mittel_wert = (np.max(zahl_werte) + np.min(zahl_werte)) / 2  # Mittlerer Wert der Zahlen der auch in die csv muss
        variabilität = np.std(zahl_werte)  # Variabilität der Zahlen - muss auch in csv

        X = np.array([[mittel_wert, variabilität] for _ in range(1000)])  # Matrix von Eigenschaften
        y = zahl_werte  # Vektor von Zahlen

        # Lade das Dataset und trainiere ein k-NN-Modell
        from sklearn.neighbors import KNeighborsRegressor
        knn = KNeighborsRegressor(n_neighbors=5)#erzeugen mit 5 nachbarn
        knn.fit(X, y)

        def vorhersage(eigenschaften):
            return knn.predict(np.array([eigenschaften]))

        # Eigenschaften der Zahl, die du erraten möchtest (z.B. mittlerer Wert, Variabilität, usw.)
        eigenschaften = [mittel_wert, variabilität]  # Mittlerer Wert und Variabilität
        vorhersagte_zahl = vorhersage(eigenschaften)
        zahlcom = vorhersagte_zahl[0]

    

    #result_label.config(text=f"Meine Ratezahl: {zahlcom}")
    tippse(result_label, f"Meine Ratezahl: {zahlcom}", 50)
    #result2_label.config(text="Ist meine Zahl zu groß oder zu klein?")
    tippse(result2_label, "Ist meine Zahl zu groß oder zu klein?", 100)
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