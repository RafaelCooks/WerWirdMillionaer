"""
import tkinter as tk
from random import randint, choice
from functools import partial


QUESTIONS = {
    1: {
        "Question": "In welcher deutschen Stadt wurde der Reichstag verhÃ¼llt?",
        "Answers": [
                ['A:', 'Bonn', False], 
                ['B:', 'Berlin', True],
                ['C:', 'Hamburg', False],
                ['D:', 'MÃ¼nchen', False]]},
    
        
                
    2: {
        "Question": "Welches Tier hat das Baden WÃ¼rttenberg im Wappen?",
        "Answers": [
                ['A:', 'Adler', False], 
                ['B:', 'Fisch', False],
                ['C:', 'BÃ¤r', False],
                ['D:', 'LÃ¶we', True]]},
                
    3: {
        "Question": "Was gilt als KÃ¶nig der Tiere ?",
        "Answers": [
                ['A:', 'Vogel', False], 
                ['B:', 'LÃ¶we', True],
                ['C:', 'Katze', False],
                ['D:', 'Schwein', False]]},
                
    4: {
        "Question": "Welches Tier rollt sich bei Gefahr zu einer Kugel?",
        "Answers": [
                ['A:', 'Pferd', False], 
                ['B:', 'Katze', False],
                ['C:', 'Igel', True],
                ['D:', 'Affe', False]]},

    5:  {
        "Question": "Wenn das Wetter gut ist, wird der Bauer bestimmt den Eber, das Ferkel und ...?",
        "Answers": [
                ['A:', 'einen drauf machen', False],
                ['B:', 'die Nacht durchmache', False],
                ['C:', 'die sau rauslassen', True],
                ['D:', 'auf die Kacke hauen', False]]},
    

    6:  {
        "Question": "Was war bereits seit Mai 1969 ein beliebtes Zahlungsmittel im europÃ¤ischen Raum?",
        "Answers":  [
                ['A:', 'Euronoten', False],
                ['B:', 'Eurocheques', True],
                ['C:', 'Euroscheine', False],
                ['D:', 'EuromÃ¼nzen', False]]},

    7:  {
        "Question": "Malu Dreyer profitierte Anfang des Jahres von ...?",
        "Answers":  [
                ['A:', 'Oettingers Sattelstang', False],
                ['B:', 'Veltins Fahrradkette', False],
                ['C:', 'Diebels Vorderreifen', False],
                ['D:', 'Becks RÃ¼cktritt', True]]}
    
            }

def create_dialog(key, callback):
    
    dialog_win = tk.Toplevel()
    dialog_win.title('Frage-{0}'.format(key))
    
    
    question = QUESTIONS[key]["Question"]
    
    frame = tk.Frame(dialog_win)
    frame.pack(padx=20, pady=10)
    
    tk.Label(frame, text=question, font=('Helvetica', 14, 'bold'),
        fg='red').pack(padx=20, pady=10)
    
    [tk.Button(frame, text=nr+answer, command=partial(callback, check,
        dialog_win)).pack(fill='x', padx=40, pady=30)
            for nr, answer, check in QUESTIONS[key]["Answers"]]    

def ask_question(check=None, dialog=None):
    
    if check is None:
        create_dialog(choice(QUESTIONS.keys()), ask_question)
        return
    
    dialog.destroy()
        
    if check:
        create_dialog(choice(QUESTIONS.keys()), ask_question)
    
    
app_win=tk.Tk()
app_win.title("Wer wird MillionÃ¤r!")

back_gnd = tk.Canvas(app_win)
back_gnd.pack(expand=True, fill='both')

#back_gnd_image = tk.PhotoImage(file="www.gif")
#back_gnd.create_image(0, 0, anchor='nw', image=back_gnd_image)


tk.Button(app_win,text='Spielen',command=ask_question).pack(expand=True)
tk.Button(app_win,text='Verlassen',command=app_win.destroy).pack(expand=True)

app_win.geometry('250x150-650+200')
app_win.mainloop()




import tkinter as tk
from tkinter import messagebox

# Fragen, Antworten und richtige Lösung
fragen = [
    {
        "frage": "Was ist die Hauptstadt von Frankreich?",
        "antworten": ["Paris", "London", "Berlin", "Madrid"],
        "richtig": "Paris"
    },
    {
        "frage": "Welcher Planet ist der Sonne am nächsten?",
        "antworten": ["Venus", "Mars", "Merkur", "Jupiter"],
        "richtig": "Merkur"
    },
    {
        "frage": "Wie viele Kontinente gibt es?",
        "antworten": ["5", "6", "7", "8"],
        "richtig": "7"
    },
    {
        "frage": "In welchem Jahr begann der Zweite Weltkrieg?",
        "antworten": ["1935", "1939", "1941", "1945"],
        "richtig": "1939"
    }
]

class MillionaireGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Wer wird Millionär")
        self.frage_index = 0

        self.frage_label = tk.Label(root, text="", wraplength=400, font=("Arial", 14))
        self.frage_label.pack(pady=20)

        self.buttons = []
        for i in range(4):
            btn = tk.Button(root, text="", width=30, font=("Arial", 12), command=lambda i=i: self.antwort_pruefen(i))
            btn.pack(pady=5)
            self.buttons.append(btn)

        self.naechste_frage()

    def naechste_frage(self):
        if self.frage_index < len(fragen):
            aktuelle_frage = fragen[self.frage_index]
            self.frage_label.config(text=aktuelle_frage["frage"])
            for i in range(4):
                self.buttons[i].config(text=aktuelle_frage["antworten"][i])
        else:
            messagebox.showinfo("Spiel beendet", "Herzlichen Glückwunsch! Du hast alle Fragen richtig beantwortet.")
            self.root.quit()

    def antwort_pruefen(self, auswahl_index):
        ausgewaehlt = self.buttons[auswahl_index].cget("text")
        richtige_antwort = fragen[self.frage_index]["richtig"]
        if ausgewaehlt == richtige_antwort:
            self.frage_index += 1
            self.naechste_frage()
        else:
            messagebox.showerror("Falsch!", f"Leider falsch! Die richtige Antwort war: {richtige_antwort}")
            self.root.quit()

# Hauptfenster starten
if __name__ == "__main__":
    root = tk.Tk()
    app = MillionaireGame(root)
    root.mainloop()
"""


import tkinter as tk
from tkinter import messagebox
import random

# Fragen-Datenbank
fragen_datenbank = {
    "leicht": [
        {"frage": "Was ist die Hauptstadt von Frankreich?", "antworten": ["Paris", "London", "Berlin", "Madrid"], "richtig": "Paris"},
        {"frage": "Wie viele Beine hat eine Spinne?", "antworten": ["6", "8", "10", "12"], "richtig": "8"},
        {"frage": "Welche Farbe entsteht aus Blau und Gelb?", "antworten": ["Grün", "Orange", "Violett", "Schwarz"], "richtig": "Grün"},
        {"frage": "Was trinkt eine Kuh?", "antworten": ["Wasser", "Milch", "Saft", "Benzin"], "richtig": "Wasser"},
        {"frage": "Welches Tier ist ein Haustier?", "antworten": ["Hund", "Tiger", "Hai", "Löwe"], "richtig": "Hund"},
        {"frage": "Was benutzt man zum Schreiben?", "antworten": ["Stift", "Löffel", "Hammer", "Pfanne"], "richtig": "Stift"}
    ],
    "mittel": [
        {"frage": "Welcher Planet ist der größte im Sonnensystem?", "antworten": ["Mars", "Jupiter", "Erde", "Venus"], "richtig": "Jupiter"},
        {"frage": "Wer malte die Mona Lisa?", "antworten": ["Leonardo da Vinci", "Picasso", "Van Gogh", "Michelangelo"], "richtig": "Leonardo da Vinci"},
        {"frage": "Wie viele Bundesländer hat Deutschland?", "antworten": ["14", "15", "16", "17"], "richtig": "16"},
        {"frage": "In welchem Jahr fiel die Berliner Mauer?", "antworten": ["1987", "1989", "1991", "1993"], "richtig": "1989"},
        {"frage": "Welcher Kontinent ist der größte?", "antworten": ["Afrika", "Asien", "Europa", "Amerika"], "richtig": "Asien"},
        {"frage": "Was ist ein Synonym für 'beginnen'?", "antworten": ["starten", "schlafen", "rennen", "hören"], "richtig": "starten"}
    ],
    "schwer": [
        {"frage": "Wie heißt das chemische Element mit dem Symbol 'Au'?", "antworten": ["Gold", "Silber", "Kupfer", "Eisen"], "richtig": "Gold"},
        {"frage": "Wer schrieb 'Faust'?", "antworten": ["Goethe", "Schiller", "Heine", "Lessing"], "richtig": "Goethe"},
        {"frage": "Welche Zahl ist eine Primzahl?", "antworten": ["21", "23", "27", "33"], "richtig": "23"},
        {"frage": "Was ist die Quadratwurzel von 144?", "antworten": ["10", "11", "12", "13"], "richtig": "12"},
        {"frage": "Wie heißt der längste Fluss der Welt?", "antworten": ["Nil", "Amazonas", "Jangtse", "Mississippi"], "richtig": "Amazonas"},
        {"frage": "Wer entwickelte die Relativitätstheorie?", "antworten": ["Newton", "Einstein", "Tesla", "Bohr"], "richtig": "Einstein"}
    ]
}

# Geldleiter (passend zu 12 Fragen)
geldleiter = [
    "100 €", "200 €", "300 €", "500 €",  # leicht
    "1.000 €", "2.000 €", "4.000 €", "8.000 €",  # mittel
    "16.000 €", "32.000 €", "64.000 €", "125.000 €"  # schwer
]

# Farben für Schwierigkeitsstufen
farben = {
    "leicht": "#4CAF50",  # grün
    "mittel": "#FFC107",  # gelb
    "schwer": "#F44336"   # rot
}

class MillionaireGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Wer wird Millionär")
        self.frage_index = 0
        self.leben = 3
        self.alle_fragen = self.generate_questions()

        # UI Elemente
        self.frage_label = tk.Label(root, text="", wraplength=500, font=("Arial", 14))
        self.frage_label.pack(pady=20)

        self.buttons = []
        for i in range(4):
            btn = tk.Button(root, text="", width=40, font=("Arial", 12), command=lambda i=i: self.antwort_pruefen(i))
            btn.pack(pady=5)
            self.buttons.append(btn)

        # Leben- und Geldleiteranzeige
        self.status_label = tk.Label(root, text=f"Leben: {self.leben} | Aktueller Gewinn: 0 €", font=("Arial", 12))
        self.status_label.pack(pady=15)

        self.naechste_frage()

    def generate_questions(self):
        # 4 aus jeder Kategorie zufällig wählen (ohne Wiederholung)
        selected_questions = []
        selected_questions += random.sample(fragen_datenbank["leicht"], 4)
        selected_questions += random.sample(fragen_datenbank["mittel"], 4)
        selected_questions += random.sample(fragen_datenbank["schwer"], 4)
        return selected_questions

    def get_schwierigkeit(self):
        # Gibt die Schwierigkeit der aktuellen Frage zurück, abhängig vom Index
        if self.frage_index < 4:
            return "leicht"
        elif self.frage_index < 8:
            return "mittel"
        else:
            return "schwer"

    def naechste_frage(self):
        if self.frage_index < len(self.alle_fragen):
            aktuelle_frage = self.alle_fragen[self.frage_index]
            schwierigkeit = self.get_schwierigkeit()
            # Frage farblich markieren
            self.frage_label.config(
                text=f"Frage {self.frage_index + 1}: {aktuelle_frage['frage']}",
                fg=farben[schwierigkeit]
            )
            for i in range(4):
                self.buttons[i].config(text=aktuelle_frage["antworten"][i])

            self.update_status()
        else:
            gewinn = geldleiter[self.frage_index-1] if self.frage_index > 0 else "0 €"
            messagebox.showinfo("Spiel beendet", f"Herzlichen Glückwunsch! Du hast {gewinn} gewonnen.")
            self.root.quit()

    def update_status(self):
        gewinn = geldleiter[self.frage_index - 1] if self.frage_index > 0 else "0 €"
        self.status_label.config(text=f"Leben: {self.leben} | Aktueller Gewinn: {gewinn}")

    def antwort_pruefen(self, auswahl_index):
        aktuelle_frage = self.alle_fragen[self.frage_index]
        ausgewaehlt = self.buttons[auswahl_index].cget("text")
        if ausgewaehlt == aktuelle_frage["richtig"]:
            self.frage_index += 1
            self.naechste_frage()
        else:
            self.leben -= 1
            if self.leben > 0:
                messagebox.showwarning("Falsch!", f"Leider falsch! Die richtige Antwort war: {aktuelle_frage['richtig']}\nDu hast noch {self.leben} Leben.")
                self.update_status()
            else:
                messagebox.showerror("Game Over!", f"Du hast keine Leben mehr. Die richtige Antwort war: {aktuelle_frage['richtig']}\nDu hast {geldleiter[self.frage_index - 1] if self.frage_index > 0 else '0 €'} gewonnen.")
                self.root.quit()

if __name__ == "__main__":
    root = tk.Tk()
    app = MillionaireGame(root)
    root.mainloop()
