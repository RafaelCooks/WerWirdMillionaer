import tkinter as tk
from tkinter import messagebox
import random
import json

# Fragen-Datenbank aus externer JSON-Datei laden
with open("fragen_beispiel.json", "r" , encoding="utf-8") as f:
    fragen_datenbank = json.load(f)

# Geldleiter (passend zu 12 Fragen)
geldleiter = [
    "100 €", "200 €", "300 €", "500 €", "1.000",  # leicht
    "2.000 €", "4.000 €", "8.000 €", "16.000 €", "32.000 €",  # mittel
    "64.000 €", "125.000 €", "250.000 €", "500.000 €", "1.000.000 €"  # schwer
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
        self.status_label = tk.Label(root, text=f"| Aktueller Gewinn: 0 € |", font=("Arial", 12))
        self.status_label.pack(pady=15)

        self.naechste_frage()

    def generate_questions(self):
        # 5 aus jeder Kategorie zufällig wählen (ohne Wiederholung)
        selected_questions = []
        selected_questions += random.sample(fragen_datenbank["leicht"], 5)
        selected_questions += random.sample(fragen_datenbank["mittel"], 5)
        selected_questions += random.sample(fragen_datenbank["schwer"], 5)
        return selected_questions

    def get_schwierigkeit(self):
        # Gibt die Schwierigkeit der aktuellen Frage zurück, abhängig vom Index
        if self.frage_index < 5:
            return "leicht"
        elif self.frage_index < 10:
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
        self.status_label.config(text=f"| Aktueller Gewinn: {gewinn} |")

    def antwort_pruefen(self, auswahl_index):
        aktuelle_frage = self.alle_fragen[self.frage_index]
        ausgewaehlt = self.buttons[auswahl_index].cget("text")
        if ausgewaehlt == aktuelle_frage["richtig"]:
            self.frage_index += 1
            self.naechste_frage()
        else:
            messagebox.showerror("Game Over!", f"Die richtige Antwort war: {aktuelle_frage['richtig']}\nDu hast {geldleiter[self.frage_index - 1] if self.frage_index > 0 else '0 €'} gewonnen.")
            self.root.quit()

if __name__ == "__main__":
    root = tk.Tk()
    app = MillionaireGame(root)
    root.mainloop()
