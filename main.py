import tkinter as tk
from tkinter import messagebox
import random
import json

with open("fragen_beispiel.json", "r", encoding="utf-8") as f:
    fragen_datenbank = json.load(f)

geldleiter = [
    "100 €", "200 €", "300 €", "500 €", "1.000 €",
    "2.000 €", "4.000 €", "8.000 €", "16.000 €", "32.000 €",
    "64.000 €", "125.000 €", "250.000 €", "500.000 €", "1.000.000 €"
]

farben = {
    "leicht": "#4CAF50",
    "mittel": "#FFC107",
    "schwer": "#F44336"
}


class StartMenu:
    def __init__(self, master, start_callback):
        self.master = master
        self.start_callback = start_callback
        self.frame = tk.Frame(master, bg="#1b1f3b")
        self.frame.pack(fill="both", expand=True)

        title = tk.Label(self.frame, text="💰 Wer wird Millionär 💰", font=("Segoe UI", 32, "bold"),
                         fg="white", bg="#1b1f3b")
        title.pack(pady=100)

        start_button = tk.Button(self.frame, text="Spiel starten", font=("Segoe UI", 18),
                                 bg="#4CAF50", fg="white", padx=20, pady=10,
                                 command=self.start_game)
        start_button.pack()

    def start_game(self):
        self.frame.destroy()
        self.start_callback()


class MillionaireGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Wer wird Millionär")
        self.root.geometry("1080x720")
        self.root.config(bg="#1b1f3b")

        self.frage_index = 0
        self.alle_fragen = self.generate_questions()
        self.timer_seconds = 0
        self.timer_id = None

        self.setup_ui()
        self.naechste_frage()

    def generate_questions(self):
        return (
            random.sample(fragen_datenbank["leicht"], 5) +
            random.sample(fragen_datenbank["mittel"], 5) +
            random.sample(fragen_datenbank["schwer"], 5)
        )

    def setup_ui(self):
        # Hauptlayout mit Frage & Antworten
        self.main_frame = tk.Frame(self.root, bg="#1b1f3b")
        self.main_frame.pack(side="left", fill="both", expand=True)

        self.frage_label = tk.Label(self.main_frame, text="", font=("Segoe UI", 20, "bold"),
                                    wraplength=700, fg="white", bg="#1b1f3b", justify="center")
        self.frage_label.pack(pady=30)

        self.buttons_frame = tk.Frame(self.main_frame, bg="#1b1f3b")
        self.buttons_frame.pack()

        self.buttons = []
        for i in range(4):
            btn = tk.Button(self.buttons_frame, text="", font=("Segoe UI", 14), width=35, height=2,
                            bg="#3a3f78", fg="white", activebackground="#6c63ff", bd=0,
                            command=lambda i=i: self.antwort_pruefen(i))
            btn.grid(row=i//2, column=i % 2, padx=20, pady=15)
            self.buttons.append(btn)

        self.timer_label = tk.Label(self.main_frame, text="", font=("Segoe UI", 16, "bold"),
                                    bg="#1b1f3b", fg="white")
        self.timer_label.pack(pady=20)

        # Sidebar für Geldleiter
        self.sidebar = tk.Frame(self.root, width=200, bg="#121428")
        self.sidebar.pack(side="right", fill="y")

        self.geldleiter_labels = []
        for i, betrag in reversed(list(enumerate(geldleiter))):
            lbl = tk.Label(self.sidebar, text=f"{i+1}. {betrag}", font=("Segoe UI", 12),
                           bg="#121428", fg="white", anchor="w", padx=10)
            lbl.pack(fill="x", pady=2)
            self.geldleiter_labels.insert(0, lbl)

    def get_schwierigkeit(self):
        if self.frage_index < 5:
            return "leicht"
        elif self.frage_index < 10:
            return "mittel"
        else:
            return "schwer"

    def naechste_frage(self):
        if self.frage_index >= len(self.alle_fragen):
            self.zeige_ende(True)
            return

        frage = self.alle_fragen[self.frage_index]
        schwierigkeit = self.get_schwierigkeit()

        self.timer_seconds = {"leicht": 10, "mittel": 20, "schwer": 30}[schwierigkeit]

        self.frage_label.config(
            text=f"Frage {self.frage_index + 1}: {frage['frage']}",
            fg=farben[schwierigkeit]
        )

        for i in range(4):
            self.buttons[i].config(text=frage["antworten"][i], state="normal", bg="#3a3f78")

        self.highlight_geldstufe()
        self.update_timer()

    def update_timer(self):
        if self.timer_seconds <= 5:
            self.timer_label.config(fg="red" if self.timer_seconds % 2 == 0 else "white")
        else:
            self.timer_label.config(fg="white")

        self.timer_label.config(text=f"⏱️ Zeit: {self.timer_seconds}s")
        if self.timer_seconds > 0:
            self.timer_seconds -= 1
            self.timer_id = self.root.after(1000, self.update_timer)
        else:
            self.zeige_ende(False, grund="Zeit abgelaufen!")

    def antwort_pruefen(self, index):
        if self.timer_id:
            self.root.after_cancel(self.timer_id)

        frage = self.alle_fragen[self.frage_index]
        ausgewaehlt = self.buttons[index].cget("text")
        richtig = frage["richtig"]

        for btn in self.buttons:
            btn.config(state="disabled")

        if ausgewaehlt == richtig:
            self.buttons[index].config(bg="#4CAF50")
            self.root.after(1000, self.frage_richtig)
        else:
            self.buttons[index].config(bg="#F44336")
            for btn in self.buttons:
                if btn.cget("text") == richtig:
                    btn.config(bg="#4CAF50")
            self.root.after(1500, lambda: self.zeige_ende(False, richtig))

    def frage_richtig(self):
        self.frage_index += 1
        self.naechste_frage()

    def highlight_geldstufe(self):
        for i, lbl in enumerate(self.geldleiter_labels):
            if i == self.frage_index:
                lbl.config(bg="#FFD700", fg="#000")
            else:
                lbl.config(bg="#121428", fg="white")

    def zeige_ende(self, gewonnen, grund=None):
        for btn in self.buttons:
            btn.config(state="disabled")

        if self.timer_id:
            self.root.after_cancel(self.timer_id)

        msg = ""
        if gewonnen:
            msg = f"🎉 Herzlichen Glückwunsch!\nDu hast {geldleiter[-1]} gewonnen!"
        else:
            gewinn = geldleiter[self.frage_index - 1] if self.frage_index > 0 else "0 €"
            msg = f"❌ Spiel beendet!\nDu hast {gewinn} gewonnen.\n"
            if grund:
                msg += f"\nGrund: {grund}"

        popup = tk.Toplevel(self.root)
        popup.geometry("500x300")
        popup.configure(bg="#1b1f3b")
        popup.title("Spiel vorbei")

        label = tk.Label(popup, text=msg, font=("Segoe UI", 16), bg="#1b1f3b", fg="white", wraplength=400)
        label.pack(pady=40)

        btn = tk.Button(popup, text="Spiel beenden", command=self.root.quit,
                        font=("Segoe UI", 12), bg="#f44336", fg="white", padx=20, pady=10)
        btn.pack(pady=20)


def main():
    root = tk.Tk()

    def start_game():
        MillionaireGame(root)

    StartMenu(root, start_game)
    root.mainloop()


if __name__ == "__main__":
    main()
