import tkinter as tk
import random
import json

with open("fragenkatalog.json", "r", encoding="utf-8") as f:
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


class MainApp:
    def __init__(self, root):
        self.root = root
        self.root.attributes('-fullscreen', True)
        self.root.configure(bg="#1b1f3b")

        self.container = tk.Frame(root, bg="#1b1f3b")
        self.container.pack(fill="both", expand=True)

        self.current_frame = None
        self.fade_step = 0.05

        self.show_start_menu()

    def fade_out_in(self, new_frame_class):
        if self.current_frame:
            self._fade_out(lambda: self._switch_frame(new_frame_class))
        else:
            self._switch_frame(new_frame_class)

    def _switch_frame(self, new_frame_class):
        if self.current_frame:
            self.current_frame.place_forget()
            self.current_frame.destroy()

        self.current_frame = new_frame_class(self.container, self)
        self.current_frame.place(relwidth=1, relheight=1)
        self._fade_in()

    def _fade_out(self, callback, alpha=1.0):
        if alpha <= 0:
            callback()
        else:
            self.root.attributes('-alpha', alpha)
            self.root.after(20, lambda: self._fade_out(callback, alpha - self.fade_step))

    def _fade_in(self, alpha=0.0):
        if alpha >= 1:
            self.root.attributes('-alpha', 1)
        else:
            self.root.attributes('-alpha', alpha)
            self.root.after(20, lambda: self._fade_in(alpha + self.fade_step))

    def show_start_menu(self):
        self.fade_out_in(StartMenu)

    def show_game(self):
        self.fade_out_in(MillionaireGame)

    def show_end(self, gewonnen, betrag, grund=""):
        self.fade_out_in(lambda parent, app: EndScreen(parent, app, gewonnen, betrag, grund))


class StartMenu(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, bg="#1b1f3b")
        self.app = app

        title = tk.Label(self, text="💰 Wer wird Millionär 💰", font=("Segoe UI", 42, "bold"),
                         fg="white", bg="#1b1f3b")
        title.pack(pady=120)

        start_button = tk.Button(self, text="Spiel starten", font=("Segoe UI", 20),
                                 bg="#4CAF50", fg="white", padx=30, pady=15,
                                 command=app.show_game)
        start_button.pack()


class MillionaireGame(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, bg="#1b1f3b")
        self.app = app
        self.frage_index = 0
        self.alle_fragen = self.generate_questions()
        self.timer_seconds = 0
        self.timer_id = None

        self.setup_ui()
        self.naechste_frage()

    def generate_questions(self):
        return (
            random.sample(fragen_datenbank["leicht"], 5) +
            random.sample(fragen_datenbank["leicht"], 5) +
            random.sample(fragen_datenbank["leicht"], 5)
        )

    def setup_ui(self):
        self.main_frame = tk.Frame(self, bg="#1b1f3b")
        self.main_frame.pack(side="left", fill="both", expand=True)

        self.frage_label = tk.Label(self.main_frame, text="", font=("Segoe UI", 22, "bold"),
                                    wraplength=900, fg="white", bg="#1b1f3b", justify="center")
        self.frage_label.pack(pady=30)

        self.buttons_frame = tk.Frame(self.main_frame, bg="#1b1f3b")
        self.buttons_frame.pack()

        self.buttons = []
        for i in range(4):
            btn = tk.Button(self.buttons_frame, text="", font=("Segoe UI", 16), width=35, height=2,
                            bg="#3a3f78", fg="white", activebackground="#6c63ff", bd=0,
                            command=lambda i=i: self.antwort_pruefen(i))
            btn.grid(row=i//2, column=i % 2, padx=20, pady=15)
            self.buttons.append(btn)

        self.timer_label = tk.Label(self.main_frame, text="", font=("Segoe UI", 16, "bold"),
                                    bg="#1b1f3b", fg="white")
        self.timer_label.pack(pady=20)

        self.sidebar = tk.Frame(self, width=200, bg="#121428")
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
            self.app.show_end(True, geldleiter[-1])
            return

        frage = self.alle_fragen[self.frage_index]
        schwierigkeit = self.get_schwierigkeit()

        self.timer_seconds = {"leicht": 10, "mittel": 20, "schwer": 30}[schwierigkeit]

        self.frage_label.config(
            text=f"Frage {self.frage_index + 1}: {frage['frage']}",
            fg=farben[schwierigkeit]
        )

        # Antworten mischen
        antworten = frage["antworten"][:]
        random.shuffle(antworten)

        # Neue richtige Antwort merken
        frage["gemischte_antworten"] = antworten
        frage["richtig"] = frage["richtig"]  # bleibt gleich, aber prüfen gegen neue Liste

        # Buttons setzen
        for i in range(4):
            self.buttons[i].config(text=antworten[i], state="normal", bg="#3a3f78")


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
            self.timer_id = self.after(1000, self.update_timer)
        else:
            self.app.show_end(False, geldleiter[self.frage_index - 1] if self.frage_index > 0 else "0 €", "Zeit abgelaufen!")

    def antwort_pruefen(self, index):
        if self.timer_id:
            self.after_cancel(self.timer_id)

        frage = self.alle_fragen[self.frage_index]
        ausgewaehlt = self.buttons[index].cget("text")
        richtig = frage["richtig"]

        for btn in self.buttons:
            btn.config(state="disabled")

        if ausgewaehlt == richtig:
            self.buttons[index].config(bg="#4CAF50")
            self.after(1000, self.frage_richtig)
        else:
            self.buttons[index].config(bg="#F44336")
            for btn in self.buttons:
                if btn.cget("text") == richtig:
                    btn.config(bg="#4CAF50")
            self.after(1500, lambda: self.app.show_end(False, geldleiter[self.frage_index - 1] if self.frage_index > 0 else "0 €", "Falsche Antwort"))

    def frage_richtig(self):
        self.frage_index += 1
        self.naechste_frage()

    def highlight_geldstufe(self):
        for i, lbl in enumerate(self.geldleiter_labels):
            if i == self.frage_index:
                lbl.config(bg="#FFD700", fg="#000")
            else:
                lbl.config(bg="#121428", fg="white")


class EndScreen(tk.Frame):
    def __init__(self, parent, app, gewonnen, betrag, grund=""):
        super().__init__(parent, bg="#1b1f3b")
        msg = ""
        if gewonnen:
            msg = f"🎉 Herzlichen Glückwunsch!\nDu hast {betrag} gewonnen!"
        else:
            msg = f"❌ Spiel beendet!\nDu hast {betrag} gewonnen."
            if grund:
                msg += f"\n\nGrund: {grund}"

        label = tk.Label(self, text=msg, font=("Segoe UI", 20), bg="#1b1f3b", fg="white", wraplength=800, justify="center")
        label.pack(pady=100)

        button_frame = tk.Frame(self, bg="#1b1f3b")
        button_frame.pack(pady=40)

        quit_btn = tk.Button(button_frame, text="Beenden", font=("Segoe UI", 14),
                             bg="#f44336", fg="white", padx=20, pady=10,
                             command=app.root.quit)
        quit_btn.pack(side="left", padx=20)

        restart_btn = tk.Button(button_frame, text="Neustart", font=("Segoe UI", 14),
                                bg="#4CAF50", fg="white", padx=20, pady=10,
                                command=app.show_start_menu)
        restart_btn.pack(side="left", padx=20)


def main():
    root = tk.Tk()
    app = MainApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
